from fastapi import FastAPI, WebSocket
from typing import List, Dict


class ConnectionManager:
    def __init__(self):
        # self.active_connections = []
        self.active_connections: List[(WebSocket, str)] = []

    async def connect(self, ws: WebSocket, user: str=None):
        # 链接
        await ws.accept()
        self.active_connections.append((ws, user))

    def disconnect(self,  ws: WebSocket, user: str=None):
        self.active_connections.remove((ws, user))

    async def broadcast(self, data: bytes):
        for connection in self.active_connections:
            # dict
            # await connection['ws'].send_bytes(data)
            # list
            await connection[0].send_bytes(data)
