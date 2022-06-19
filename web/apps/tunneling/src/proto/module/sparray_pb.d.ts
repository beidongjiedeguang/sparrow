import * as jspb from 'google-protobuf'

import * as google_protobuf_struct_pb from 'google-protobuf/google/protobuf/struct_pb';


export class DenseNdArrayProto extends jspb.Message {
  getBuffer(): Uint8Array | string;
  getBuffer_asU8(): Uint8Array;
  getBuffer_asB64(): string;
  setBuffer(value: Uint8Array | string): DenseNdArrayProto;

  getShapeList(): Array<number>;
  setShapeList(value: Array<number>): DenseNdArrayProto;
  clearShapeList(): DenseNdArrayProto;
  addShape(value: number, index?: number): DenseNdArrayProto;

  getDtype(): string;
  setDtype(value: string): DenseNdArrayProto;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): DenseNdArrayProto.AsObject;
  static toObject(includeInstance: boolean, msg: DenseNdArrayProto): DenseNdArrayProto.AsObject;
  static serializeBinaryToWriter(message: DenseNdArrayProto, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): DenseNdArrayProto;
  static deserializeBinaryFromReader(message: DenseNdArrayProto, reader: jspb.BinaryReader): DenseNdArrayProto;
}

export namespace DenseNdArrayProto {
  export type AsObject = {
    buffer: Uint8Array | string,
    shapeList: Array<number>,
    dtype: string,
  }
}

export class DocProto extends jspb.Message {
  getId(): string;
  setId(value: string): DocProto;

  getBlob(): Uint8Array | string;
  getBlob_asU8(): Uint8Array;
  getBlob_asB64(): string;
  setBlob(value: Uint8Array | string): DocProto;

  getTensor(): DenseNdArrayProto | undefined;
  setTensor(value?: DenseNdArrayProto): DocProto;
  hasTensor(): boolean;
  clearTensor(): DocProto;

  getText(): string;
  setText(value: string): DocProto;

  getContentCase(): DocProto.ContentCase;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): DocProto.AsObject;
  static toObject(includeInstance: boolean, msg: DocProto): DocProto.AsObject;
  static serializeBinaryToWriter(message: DocProto, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): DocProto;
  static deserializeBinaryFromReader(message: DocProto, reader: jspb.BinaryReader): DocProto;
}

export namespace DocProto {
  export type AsObject = {
    id: string,
    blob: Uint8Array | string,
    tensor?: DenseNdArrayProto.AsObject,
    text: string,
  }

  export enum ContentCase { 
    CONTENT_NOT_SET = 0,
    BLOB = 2,
    TENSOR = 3,
    TEXT = 4,
  }
}

export class DocArrayProto extends jspb.Message {
  getDocsList(): Array<DocProto>;
  setDocsList(value: Array<DocProto>): DocArrayProto;
  clearDocsList(): DocArrayProto;
  addDocs(value?: DocProto, index?: number): DocProto;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): DocArrayProto.AsObject;
  static toObject(includeInstance: boolean, msg: DocArrayProto): DocArrayProto.AsObject;
  static serializeBinaryToWriter(message: DocArrayProto, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): DocArrayProto;
  static deserializeBinaryFromReader(message: DocArrayProto, reader: jspb.BinaryReader): DocArrayProto;
}

export namespace DocArrayProto {
  export type AsObject = {
    docsList: Array<DocProto.AsObject>,
  }
}

