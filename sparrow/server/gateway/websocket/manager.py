from fastapi import FastAPI, WebSocket
from typing import List, Dict


class ConnectionManager:
    def __init__(self):
        # 存放**的链接
        self.active_connections: List[Dict[str, WebSocket]] = []

    async def connect(self, ws: WebSocket, user: str=None):
        # 链接
        await ws.accept()
        if user is None:
            self.active_connections.append(ws)
        else:
            self.active_connections.append({"user": user, "ws": ws})



    def disconnect(self,  ws: WebSocket, user: str=None):
        if user is not None:
            self.active_connections.remove({"user": user, "ws": ws})
        else:
            self.active_connections.remove(ws)


    @staticmethod
    async def send_personal_message(message: str, ws: WebSocket):
        # 发送所有人消息
        await ws.send_bytes(message)

    async def send_other_message(self, message: dict, user: str=None):
        # 发送个人消息
        for connection in self.active_connections:
            if user is not None:
                if connection["user"] == user:
                    await connection['ws'].send_bytes(message)
            else:
                await ws.send_bytes(message)

    async def broadcast(self, data: bytes):
        for connection in self.active_connections:
            # dict
            # await connection['ws'].send_bytes(data)
            # list
            await connection.send_bytes(data)
