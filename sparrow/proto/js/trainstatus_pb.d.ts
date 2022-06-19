import * as jspb from 'google-protobuf'



export class TrainStatus extends jspb.Message {
  getFinished(): boolean;
  setFinished(value: boolean): TrainStatus;

  getStep(): number;
  setStep(value: number): TrainStatus;

  getLoss(): number;
  setLoss(value: number): TrainStatus;

  getProgress(): number;
  setProgress(value: number): TrainStatus;

  getCostTime(): number;
  setCostTime(value: number): TrainStatus;

  getMsg(): string;
  setMsg(value: string): TrainStatus;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): TrainStatus.AsObject;
  static toObject(includeInstance: boolean, msg: TrainStatus): TrainStatus.AsObject;
  static serializeBinaryToWriter(message: TrainStatus, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): TrainStatus;
  static deserializeBinaryFromReader(message: TrainStatus, reader: jspb.BinaryReader): TrainStatus;
}

export namespace TrainStatus {
  export type AsObject = {
    finished: boolean,
    step: number,
    loss: number,
    progress: number,
    costTime: number,
    msg: string,
  }
}

export class HttpResponse extends jspb.Message {
  getCode(): number;
  setCode(value: number): HttpResponse;

  getMsg(): string;
  setMsg(value: string): HttpResponse;

  getData(): TrainStatus | undefined;
  setData(value?: TrainStatus): HttpResponse;
  hasData(): boolean;
  clearData(): HttpResponse;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): HttpResponse.AsObject;
  static toObject(includeInstance: boolean, msg: HttpResponse): HttpResponse.AsObject;
  static serializeBinaryToWriter(message: HttpResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): HttpResponse;
  static deserializeBinaryFromReader(message: HttpResponse, reader: jspb.BinaryReader): HttpResponse;
}

export namespace HttpResponse {
  export type AsObject = {
    code: number,
    msg: string,
    data?: TrainStatus.AsObject,
  }
}

