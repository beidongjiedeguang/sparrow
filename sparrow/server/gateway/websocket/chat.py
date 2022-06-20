from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from typing import List, Dict
from sparrow.proto.python import trainstatus_pb2, trainstatus_pb2_grpc
from google.protobuf.internal import decoder, encoder
from sparrow import rel_to_abs
from sparrow.server.gateway.websocket.manager import ConnectionManager
import time
import random

state = trainstatus_pb2.TrainStatus()
app = FastAPI()

manager = ConnectionManager()


@app.websocket("/ws_chat")
async def websocket_endpoint_chat(websocket: WebSocket):
    await manager.connect(websocket)
    while True:
        byte_data = await websocket.receive_bytes()
        state.ParseFromString(byte_data)
        print("接收到从ts来的数据: ", state)
        state.cost_time = time.time()
        state.loss = 1.2
        state.finished = not state.finished
        state.progress = random.random()
        print("发送给ts的数据: ", state)
        print("end -----------------")
        await manager.broadcast(state.SerializeToString())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("chat:app", host="0.0.0.0", port=8000, reload=True)
