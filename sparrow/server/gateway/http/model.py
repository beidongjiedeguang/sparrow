from collections import defaultdict
from datetime import datetime
from enum import Enum
from types import SimpleNamespace
from typing import Callable, Dict, List, Optional, Union

# from docarray.document.pydantic_model import PydanticDocumentArray
from google.protobuf.descriptor import Descriptor, FieldDescriptor
from google.protobuf.pyext.cpp_message import GeneratedProtocolMessageType
from pydantic import BaseConfig, BaseModel, Field, create_model, root_validator

from sparrow.proto.python.trainstatus_pb2 import TrainStatus, HttpResponse

PROTO_TO_PYDANTIC_MODELS = SimpleNamespace()
PROTOBUF_TO_PYTHON_TYPE = {
    FieldDescriptor.TYPE_INT32: int,
    FieldDescriptor.TYPE_INT64: int,
    FieldDescriptor.TYPE_UINT32: int,
    FieldDescriptor.TYPE_UINT64: int,
    FieldDescriptor.TYPE_SINT32: int,
    FieldDescriptor.TYPE_SINT64: int,
    FieldDescriptor.TYPE_BOOL: bool,
    FieldDescriptor.TYPE_FLOAT: float,
    FieldDescriptor.TYPE_DOUBLE: float,
    FieldDescriptor.TYPE_FIXED32: float,
    FieldDescriptor.TYPE_FIXED64: float,
    FieldDescriptor.TYPE_SFIXED32: float,
    FieldDescriptor.TYPE_SFIXED64: float,
    FieldDescriptor.TYPE_BYTES: bytes,
    FieldDescriptor.TYPE_STRING: str,
    FieldDescriptor.TYPE_ENUM: Enum,
    FieldDescriptor.TYPE_MESSAGE: None,
}


class CustomConfig(BaseConfig):
    """Pydantic config for Camel case and enum handling"""

    use_enum_values = True
    allow_population_by_field_name = True


def _get_oneof_validator(oneof_fields: List, oneof_key: str) -> Callable:
    """
    Pydantic root validator (pre) classmethod generator to confirm only one oneof field is passed
    :param oneof_fields: list of field names for oneof
    :type oneof_fields: List
    :param oneof_key: oneof key
    :type oneof_key: str
    :return: classmethod for validating oneof fields
    """

    def oneof_validator(cls, values):
        if len(set(oneof_fields).intersection(set(values))) > 1:
            raise ValueError(
                f'only one field among {oneof_fields} can be set for key {oneof_key}!'
            )
        return values

    oneof_validator.__qualname__ = 'validate_' + oneof_key
    return root_validator(pre=True, allow_reuse=True)(oneof_validator)


def _get_oneof_setter(oneof_fields: List, oneof_key: str) -> Callable:
    """
    Pydantic root validator (post) classmethod generator to set the oneof key
    :param oneof_fields: list of field names for oneof
    :type oneof_fields: List
    :param oneof_key: oneof key
    :type oneof_key: str
    :return: classmethod for setting oneof fields in Pydantic models
    """

    def oneof_setter(cls, values):
        for oneof_field in oneof_fields:
            if (
                    oneof_field in values
                    and values[oneof_field] == cls.__fields__[oneof_field].default
            ):
                values.pop(oneof_field)
        return values

    oneof_setter.__qualname__ = 'set_' + oneof_key
    return root_validator(pre=False, allow_reuse=True)(oneof_setter)


def protobuf_to_pydantic_model(
        protobuf_model: Union[Descriptor, GeneratedProtocolMessageType]
) -> BaseModel:
    """
    Converts Protobuf messages to Pydantic model for jsonschema creation/validattion
    ..note:: Model gets assigned in the global Namespace :data:PROTO_TO_PYDANTIC_MODELS
    :param protobuf_model: message from jina.proto file
    :type protobuf_model: Union[Descriptor, GeneratedProtocolMessageType]
    :return: Pydantic model
    """

    all_fields = {}
    camel_case_fields = {}  # {"random_string": {"alias": "randomString"}}
    oneof_fields = defaultdict(list)
    oneof_field_validators = {}

    if isinstance(protobuf_model, Descriptor):
        model_name = protobuf_model.name
        protobuf_fields = protobuf_model.fields
    elif isinstance(protobuf_model, GeneratedProtocolMessageType):
        model_name = protobuf_model.DESCRIPTOR.name
        protobuf_fields = protobuf_model.DESCRIPTOR.fields

    if model_name in vars(PROTO_TO_PYDANTIC_MODELS):
        return PROTO_TO_PYDANTIC_MODELS.__getattribute__(model_name)

    for f in protobuf_fields:
        field_name = f.name
        camel_case_fields[field_name] = {'alias': f.camelcase_name}

        field_type = PROTOBUF_TO_PYTHON_TYPE[f.type]
        default_value = f.default_value
        default_factory = None

        if f.containing_oneof:
            # Proto Field type: oneof
            # NOTE: oneof fields are handled as a post-processing step
            oneof_fields[f.containing_oneof.name].append(field_name)

        if field_type is Enum:
            # Proto Field Type: enum
            enum_dict = {}

            for enum_field in f.enum_type.values:
                enum_dict[enum_field.name] = enum_field.number

            field_type = Enum(f.enum_type.name, enum_dict)

        if f.message_type:
            if f.message_type.name == 'Struct':
                # Proto Field Type: google.protobuf.Struct
                field_type = Dict
                default_factory = dict
            elif f.message_type.name == 'Timestamp':
                # Proto Field Type: google.protobuf.Timestamp
                field_type = datetime
                default_factory = datetime.now
            else:
                # Proto field type: Proto message defined in jina.proto
                if f.message_type.name == model_name:
                    # Self-referencing models
                    field_type = model_name
                else:
                    # This field_type itself a Pydantic model
                    field_type = protobuf_to_pydantic_model(f.message_type)
                    PROTO_TO_PYDANTIC_MODELS.model_name = field_type

        if f.label == FieldDescriptor.LABEL_REPEATED:
            field_type = List[field_type]

        all_fields[field_name] = (
            field_type,
            Field(default_factory=default_factory)
            if default_factory
            else Field(default=default_value),
        )

    # Post-processing (Handle oneof fields)
    for oneof_k, oneof_v_list in oneof_fields.items():
        oneof_field_validators[f'oneof_validator_{oneof_k}'] = _get_oneof_validator(
            oneof_fields=oneof_v_list, oneof_key=oneof_k
        )
        oneof_field_validators[f'oneof_setter_{oneof_k}'] = _get_oneof_setter(
            oneof_fields=oneof_v_list, oneof_key=oneof_k
        )

    CustomConfig.fields = camel_case_fields
    model = create_model(
        model_name,
        **all_fields,
        __config__=CustomConfig,
        __validators__=oneof_field_validators,
    )
    model.update_forward_refs()
    PROTO_TO_PYDANTIC_MODELS.__setattr__(model_name, model)

    return model
