#!/bin/bash

# -----------------------------------------------------------------------------
# 暂时不要用这个文件进行生成，我们暂时不需要grpc.！
# -----------------------------------------------------------------------------

# reference https://www.npmjs.com/package/protoc-gen-grpc

PROTOC_GEN_TS_PATH="./node_modules/.bin/protoc-gen-ts"

# Path to the grpc_node_plugin
PROTOC_GEN_GRPC_PATH="./node_modules/protoc-gen-grpc/bin/grpc_node_plugin"

OUT_DIR="./src/proto/modules"
#protoc \
#    --plugin="protoc-gen-ts=${PROTOC_GEN_TS_PATH}" \
#    --plugin="protoc-gen-grpc=${PROTOC_GEN_GRPC_PATH}" \
#    --js_out="import_style=commonjs,binary:${OUT_DIR}" \
#    --ts_out="service=grpc-node:${OUT_DIR}" \
#    --grpc_out="${OUT_DIR}" \
#    ./src/proto/*.proto

# another option
protoc-gen-grpc \
--js_out="import_style=commonjs,binary:${OUT_DIR}" \
--grpc_out="${OUT_DIR}" \
./src/proto/*.proto

protoc-gen-grpc-ts \
--ts_out=grpc_js:${OUT_DIR} \
./src/proto/*.proto