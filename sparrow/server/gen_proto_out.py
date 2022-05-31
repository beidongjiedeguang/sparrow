import os
from sparrow.path import rel_to_abs
from glob import glob
import shutil

proto_dir = rel_to_abs('./proto', return_str=True)
proto_list = [proto for proto in glob(os.path.join(proto_dir, '*.proto'))]
python_out = os.path.join(proto_dir, 'python')
javascript_out = os.path.join(proto_dir, 'javascript')

web_proto_path_list = glob(rel_to_abs('../../web/apps/*/src/proto', return_str=True))
# app_path_list = glob(rel_to_abs('../../web/apps/*', return_str=True))
PROTOC_GEN_TS_PATH = os.path.join(rel_to_abs('../../web/apps/chatroom', return_str=True),
                                  "node_modules/.bin/protoc-gen-ts")

for proto_path in proto_list:
    os.system(f"protoc --proto_path={proto_dir} --python_out={python_out} {proto_path}")

    os.system(f"protoc --proto_path={proto_dir} \
    --js_out=import_style=commonjs,binary:{javascript_out} \
    --ts_out={javascript_out} \
    --plugin=protoc-gen-ts={PROTOC_GEN_TS_PATH} \
    {proto_path}")

    [shutil.copy(proto_path, web_proto_path) for web_proto_path in web_proto_path_list]

# copy to web proto dir
# web_proto_path = rel_to_abs("../../web/apps/chatroom/src/proto/ts", return_str=True)
# if os.path.exists(web_proto_path):
#     shutil.rmtree(web_proto_path)
# shutil.copytree(f"{javascript_out}", web_proto_path)
