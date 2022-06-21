import os
from sparrow.path import rel_to_abs
from glob import glob
import shutil

proto_dir = rel_to_abs('.', return_str=True)
proto_list = [proto for proto in glob(os.path.join(proto_dir, '*.proto'))]


def build_python():
    python_out = os.path.join(proto_dir, 'python')
    for proto_path in proto_list:
        os.system(f"protoc --proto_path={proto_dir} --python_out={python_out} {proto_path}")
        os.system(f"python -m grpc_tools.protoc --proto_path={proto_dir} \
        --python_out={python_out} \
        --grpc_python_out={python_out} \
        {proto_path} ")


def build_web():
    # https://github.com/grpc/grpc-web
    javascript_out = os.path.join(proto_dir, 'js')
    web_proto_path_list = glob(rel_to_abs('../../web/apps/*/src/proto', return_str=True))
    PROTOC_GEN_TS_PATH = os.path.join(rel_to_abs('../../web/apps/chatroom', return_str=True),
                                      "node_modules/.bin/protoc-gen-ts")

    def gen_web_1(proto_path):
        # 可
        os.system(f"protoc --proto_path={proto_dir} \
        --js_out=import_style=commonjs,binary:{javascript_out} \
        --ts_out={javascript_out} \
        --plugin=protoc-gen-ts={PROTOC_GEN_TS_PATH} \
        {proto_path}")

    def gen_web__js(proto_path):
        # 可
        os.system(f"protoc --proto_path={proto_dir} \
        --js_out=import_style=commonjs,binary:{javascript_out} \
        --grpc-web_out=import_style=commonjs,mode=grpcwebtext:{javascript_out} \
        {proto_path}")

    def gen_web__ts(proto_path):
        # 可
        command = f"protoc --proto_path={proto_dir} \
        --js_out=import_style=commonjs:{javascript_out} \
        --grpc-web_out=import_style=typescript,mode=grpcweb:{javascript_out} \
        {proto_path}"
        os.system(command)

    for proto_path in proto_list:
        # gen_web_1(proto_path)
        gen_web__ts(proto_path)

        [shutil.copy(proto_path, web_proto_path) for web_proto_path in web_proto_path_list]

    # copy to web proto dir
    web_proto_path = rel_to_abs("../../web/apps/chatroom/src/proto/module", return_str=True)
    if os.path.exists(web_proto_path):
        shutil.rmtree(web_proto_path)
    shutil.copytree(f"{javascript_out}", web_proto_path)


def copy_proto_to_web():
    web_proto_path_list = glob(rel_to_abs('../../web/apps/*/src/proto', return_str=True))
    for proto_path in proto_list:
        [shutil.copy(proto_path, web_proto_path) for web_proto_path in web_proto_path_list]
        # for web_proto_path in web_proto_path_list:
        #     shutil.copy(proto_path, web_proto_path)


build_python()
# build_web()
copy_proto_to_web()
