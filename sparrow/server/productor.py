from sparrow.server.proto.python import trainstatus_pb2
from sparrow import rel_to_abs

state = trainstatus_pb2.TrainStatus()

state.step = 100
state.finished = True
state.progress = 0.5
state.loss = 1.2

with open(rel_to_abs("./proto/bin/train_state.bin"), "wb") as f:
    f.write(state.SerializeToString())
