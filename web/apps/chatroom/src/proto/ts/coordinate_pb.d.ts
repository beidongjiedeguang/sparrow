// package: protocoordinate
// file: coordinate.proto

import * as jspb from "google-protobuf";

export class UpdateData extends jspb.Message {
  getName(): string;
  setName(value: string): void;

  clearCoordsList(): void;
  getCoordsList(): Array<UpdateData.Coord>;
  setCoordsList(value: Array<UpdateData.Coord>): void;
  addCoords(value?: UpdateData.Coord, index?: number): UpdateData.Coord;

  clearQuaternionsList(): void;
  getQuaternionsList(): Array<UpdateData.Quaternion>;
  setQuaternionsList(value: Array<UpdateData.Quaternion>): void;
  addQuaternions(value?: UpdateData.Quaternion, index?: number): UpdateData.Quaternion;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): UpdateData.AsObject;
  static toObject(includeInstance: boolean, msg: UpdateData): UpdateData.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: UpdateData, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): UpdateData;
  static deserializeBinaryFromReader(message: UpdateData, reader: jspb.BinaryReader): UpdateData;
}

export namespace UpdateData {
  export type AsObject = {
    name: string,
    coordsList: Array<UpdateData.Coord.AsObject>,
    quaternionsList: Array<UpdateData.Quaternion.AsObject>,
  }

  export class Coord extends jspb.Message {
    getX(): number;
    setX(value: number): void;

    getY(): number;
    setY(value: number): void;

    getZ(): number;
    setZ(value: number): void;

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): Coord.AsObject;
    static toObject(includeInstance: boolean, msg: Coord): Coord.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: Coord, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): Coord;
    static deserializeBinaryFromReader(message: Coord, reader: jspb.BinaryReader): Coord;
  }

  export namespace Coord {
    export type AsObject = {
      x: number,
      y: number,
      z: number,
    }
  }

  export class Quaternion extends jspb.Message {
    getX(): number;
    setX(value: number): void;

    getY(): number;
    setY(value: number): void;

    getZ(): number;
    setZ(value: number): void;

    getW(): number;
    setW(value: number): void;

    serializeBinary(): Uint8Array;
    toObject(includeInstance?: boolean): Quaternion.AsObject;
    static toObject(includeInstance: boolean, msg: Quaternion): Quaternion.AsObject;
    static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
    static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
    static serializeBinaryToWriter(message: Quaternion, writer: jspb.BinaryWriter): void;
    static deserializeBinary(bytes: Uint8Array): Quaternion;
    static deserializeBinaryFromReader(message: Quaternion, reader: jspb.BinaryReader): Quaternion;
  }

  export namespace Quaternion {
    export type AsObject = {
      x: number,
      y: number,
      z: number,
      w: number,
    }
  }
}

