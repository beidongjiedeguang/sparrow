// package: protostatus
// file: trainstatus.proto

import * as jspb from "google-protobuf";

export class TrainStatus extends jspb.Message {
  getFinished(): boolean;
  setFinished(value: boolean): void;

  getStep(): number;
  setStep(value: number): void;

  getProgress(): number;
  setProgress(value: number): void;

  getLoss(): number;
  setLoss(value: number): void;

  getTimestamp(): number;
  setTimestamp(value: number): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): TrainStatus.AsObject;
  static toObject(includeInstance: boolean, msg: TrainStatus): TrainStatus.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: TrainStatus, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): TrainStatus;
  static deserializeBinaryFromReader(message: TrainStatus, reader: jspb.BinaryReader): TrainStatus;
}

export namespace TrainStatus {
  export type AsObject = {
    finished: boolean,
    step: number,
    progress: number,
    loss: number,
    timestamp: number,
  }
}

