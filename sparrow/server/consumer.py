from sparrow.server.proto.python import trainstatus_pb2
from sparrow import rel_to_abs
state = trainstatus_pb2.TrainStatus()


with open(rel_to_abs("./proto/bin/train_state.bin"), "rb") as f:
    state.ParseFromString(f.read())

print(state, type(state))
