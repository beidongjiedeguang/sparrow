from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from typing import List, Dict

import grpc

from sparrow.proto.python import trainstatus_pb2, trainstatus_pb2_grpc
from sparrow.proto.python.sparray_pb2 import DocProto, DocArrayProto

from google.protobuf.internal import decoder, encoder
from sparrow import rel_to_abs
import time

state = DocProto()
app = FastAPI()





def parse_proto(pb_msg: DocProto):
    fields = {}
    for field, value in pb_msg.ListFields():
        f_name = field.name
        fields[f_name] = value
    return fields


@app.websocket("/ws_tunnel")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        byte_data = await websocket.receive_bytes()
        print("start -----------------")
        print(byte_data[:100])

        state.ParseFromString(byte_data)
        print(parse_proto(state))
        print("end -----------------")

        await websocket.send_bytes(state.SerializeToString())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
