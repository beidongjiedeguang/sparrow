from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from typing import List, Dict

import grpc

from sparrow.proto.python import trainstatus_pb2, trainstatus_pb2_grpc
from sparrow.proto.python.sparray_pb2 import DocProto, DocArrayProto
from sparrow.server.gateway.websocket.manager import ConnectionManager

from google.protobuf.internal import decoder, encoder
from sparrow import rel_to_abs
import time

proto = DocProto()
app = FastAPI()
manager = ConnectionManager()


def parse_proto(pb_msg: DocProto):
    fields = {}
    for field, value in pb_msg.ListFields():
        f_name = field.name
        fields[f_name] = value
    return fields


@app.websocket("/ws_tunnel")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    while True:
        byte_data = await websocket.receive_bytes()
        print("start -----------------")
        print(byte_data[:100])
        proto.ParseFromString(byte_data)
        print("end -----------------")
        await manager.broadcast(proto.SerializeToString())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("tunnel:app", host="0.0.0.0", port=8000, reload=True)
