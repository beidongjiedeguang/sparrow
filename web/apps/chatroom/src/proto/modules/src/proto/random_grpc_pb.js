// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('grpc');
var src_proto_random_pb = require('../../src/proto/random_pb.js');

function serialize_randomPackage_PingRequest(arg) {
  if (!(arg instanceof src_proto_random_pb.PingRequest)) {
    throw new Error('Expected argument of type randomPackage.PingRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_randomPackage_PingRequest(buffer_arg) {
  return src_proto_random_pb.PingRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_randomPackage_PongResponse(arg) {
  if (!(arg instanceof src_proto_random_pb.PongResponse)) {
    throw new Error('Expected argument of type randomPackage.PongResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_randomPackage_PongResponse(buffer_arg) {
  return src_proto_random_pb.PongResponse.deserializeBinary(new Uint8Array(buffer_arg));
}


var RandomService = exports.RandomService = {
  pingPong: {
    path: '/randomPackage.Random/PingPong',
    requestStream: false,
    responseStream: false,
    requestType: src_proto_random_pb.PingRequest,
    responseType: src_proto_random_pb.PongResponse,
    requestSerialize: serialize_randomPackage_PingRequest,
    requestDeserialize: deserialize_randomPackage_PingRequest,
    responseSerialize: serialize_randomPackage_PongResponse,
    responseDeserialize: deserialize_randomPackage_PongResponse,
  },
};

exports.RandomClient = grpc.makeGenericClientConstructor(RandomService);
