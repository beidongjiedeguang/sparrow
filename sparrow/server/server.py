from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from typing import List, Dict
from sparrow.server.proto.python import trainstatus_pb2
from google.protobuf.internal import decoder, encoder
from sparrow import rel_to_abs
import time

state = trainstatus_pb2.TrainStatus()
app = FastAPI()


class ConnectionManager:
    def __init__(self):
        # 存放**的链接
        self.active_connections: List[Dict[str, WebSocket]] = []

    async def connect(self, user: str, ws: WebSocket):
        # 链接
        await ws.accept()
        self.active_connections.append({"user": user, "ws": ws})

    def disconnect(self, user: str, ws: WebSocket):
        # 关闭时 移除ws对象
        self.active_connections.remove({"user": user, "ws": ws})

    @staticmethod
    async def send_personal_message(message: str, ws: WebSocket):
        # 发送所有人消息
        await ws.send_text(message)

    async def send_other_message(self, message: dict, user: str):
        # 发送个人消息
        for connection in self.active_connections:
            if connection["user"] == user:
                await connection['ws'].send_json(message)

    async def broadcast(self, data: str):
        # 广播消息
        for connection in self.active_connections:
            await connection['ws'].send_text(data)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        byte_data = await websocket.receive_bytes()
        print("start -----------------")
        print(byte_data)

        state.ParseFromString(byte_data)
        print(state)
        state.timestamp = time.time()
        state.finished = not state.finished

        print("end -----------------")

        await websocket.send_bytes(state.SerializeToString())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
