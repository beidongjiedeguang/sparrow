// package: randomPackage
// file: src/proto/random.proto

import * as grpc from '@grpc/grpc-js';
import * as src_proto_random_pb from '../../src/proto/random_pb';

interface IRandomService extends grpc.ServiceDefinition<grpc.UntypedServiceImplementation> {
  pingPong: IRandomService_IPingPong;
}

interface IRandomService_IPingPong extends grpc.MethodDefinition<src_proto_random_pb.PingRequest, src_proto_random_pb.PongResponse> {
  path: '/randomPackage.Random/PingPong'
  requestStream: false
  responseStream: false
  requestSerialize: grpc.serialize<src_proto_random_pb.PingRequest>;
  requestDeserialize: grpc.deserialize<src_proto_random_pb.PingRequest>;
  responseSerialize: grpc.serialize<src_proto_random_pb.PongResponse>;
  responseDeserialize: grpc.deserialize<src_proto_random_pb.PongResponse>;
}

export const RandomService: IRandomService;
export interface IRandomServer extends grpc.UntypedServiceImplementation {
  pingPong: grpc.handleUnaryCall<src_proto_random_pb.PingRequest, src_proto_random_pb.PongResponse>;
}

export interface IRandomClient {
  pingPong(request: src_proto_random_pb.PingRequest, callback: (error: grpc.ServiceError | null, response: src_proto_random_pb.PongResponse) => void): grpc.ClientUnaryCall;
  pingPong(request: src_proto_random_pb.PingRequest, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: src_proto_random_pb.PongResponse) => void): grpc.ClientUnaryCall;
  pingPong(request: src_proto_random_pb.PingRequest, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: src_proto_random_pb.PongResponse) => void): grpc.ClientUnaryCall;
}

export class RandomClient extends grpc.Client implements IRandomClient {
  constructor(address: string, credentials: grpc.ChannelCredentials, options?: Partial<grpc.ClientOptions>);
  public pingPong(request: src_proto_random_pb.PingRequest, callback: (error: grpc.ServiceError | null, response: src_proto_random_pb.PongResponse) => void): grpc.ClientUnaryCall;
  public pingPong(request: src_proto_random_pb.PingRequest, metadata: grpc.Metadata, callback: (error: grpc.ServiceError | null, response: src_proto_random_pb.PongResponse) => void): grpc.ClientUnaryCall;
  public pingPong(request: src_proto_random_pb.PingRequest, metadata: grpc.Metadata, options: Partial<grpc.CallOptions>, callback: (error: grpc.ServiceError | null, response: src_proto_random_pb.PongResponse) => void): grpc.ClientUnaryCall;
}

