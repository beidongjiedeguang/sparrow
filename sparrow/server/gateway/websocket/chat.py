from pydantic import BaseModel
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse, Response
from typing import List, Dict
from sparrow.proto.python import trainstatus_pb2, trainstatus_pb2_grpc
from sparrow.proto.python.sparray_pb2 import ChatProto
from google.protobuf.internal import decoder, encoder
from sparrow import rel_to_abs
from sparrow.server.gateway.websocket.manager import ConnectionManager
import time
import random
from fastapi import (
    WebSocketDisconnect,
    Request
)

chatproto = ChatProto()
app = FastAPI()

manager = ConnectionManager()


@app.websocket("/ws_chat")
async def chat(websocket: WebSocket):
    # sender = websocket.cookies.get("X-Authorization")
    sender = "emmm"
    if sender:
        await manager.connect(websocket, sender)
        try:
            while True:
                byte_data = await websocket.receive_bytes()
                chatproto.ParseFromString(byte_data)
                # print("接收到从ts来的数据: ", chatproto)
                await manager.broadcast(chatproto.SerializeToString())
        except WebSocketDisconnect:
            manager.disconnect(websocket, sender)
            # response['message'] = "left"
            # await manager.broadcast(response)

    # await manager.connect(websocket)
    # while True:
    #     byte_data = await websocket.receive_bytes()
    #     chatproto.ParseFromString(byte_data)
    #     print("接收到从ts来的数据: ", chatproto)
    #     chatproto.cost_time = time.time()
    #     chatproto.loss = 1.2
    #     chatproto.finished = not chatproto.finished
    #     chatproto.progress = random.random()
    #     print("发送给ts的数据: ", chatproto)
    #     print("end -----------------")
    #     await manager.broadcast(chatproto.SerializeToString())
    #


@app.get("/api/current_user")
def get_user(request: Request):
    return request.cookies.get("X-Authorization")


class RegisterValidator(BaseModel):
    username: str


@app.post("/api/register")
def register_user(user: RegisterValidator, response: Response):
    response.set_cookie(key="X-Authorization", value=user.username, httponly=True)


if __name__ == "__main__":
    import uvicorn

    local = True
    if local:
        host = "0.0.0.0"
        port = 8000
        reload = True
    else:
        host = "0.0.0.0"
        port = 8080
        reload = False

    uvicorn.run("chat:app", host=host, port=port, reload=reload)
