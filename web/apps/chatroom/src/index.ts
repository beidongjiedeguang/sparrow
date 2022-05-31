import * as protobuf from 'protobufjs';

const path = require('path');
// import path from 'path';
import * as grpc from "@grpc/grpc-js";
import * as protoLoader from "@grpc/proto-loader";
import {PongResponse, PingRequest} from './proto/ts/random_pb';
import {RandomService, RandomClient} from './proto/modules/src/proto/random_grpc_pb';


const PORT = 8082;
const PROTO_FILE = './proto/random.proto';

const packageDefinition = protoLoader.loadSync(path.resolve(__dirname, PROTO_FILE));
const protoDescriptor = grpc.loadPackageDefinition(packageDefinition);
// const randomPackage = protoDescriptor.randomPackage;
// const randomService = randomPackage.Random;
function main(){
    const server = getServer();
    server.bindAsync(`0.0.0.0:${PORT}`, grpc.ServerCredentials.createInsecure(), (err, port) => {
        if (err) {
            console.log(err);
            return;
        }
        console.log(`Server listening on ${port}`);
        server.start();
    });
}

function getServer(){
    const server = new grpc.Server();
    server.addService(RandomService, {
        "PingPong": ()=> {

        }
    });
    return server
}


// func2()


function func2(){
    const date = new Date();

    protobuf.load('./proto/trainstatus.proto').then((root: any) => {

        let TrainState = root.lookupType("protostatus.TrainStatus");
        let payload = {"loss": 0.1, "step": 100, "progress": 0.99, "finished": false, "timestamp": date.getTime()/1000};
        let errMsg = TrainState.verify(payload);
        if (errMsg) {
            throw Error(errMsg);
        }
        let message = TrainState.create(payload);
        console.log(message);
        console.log(`message = ${JSON.stringify(message)}`);

        let buffer = TrainState.encode(message).finish();
        let socket = new WebSocket("ws://localhost:8000/ws");
        socket.binaryType = 'arraybuffer'

        socket.onopen = (e) => {
            socket.send(buffer);
        };

        let msg;
        socket.onmessage = async (event) => {
            alert(`[message] Data received from server: ${event.data}`);
            let arraybuffer = new Uint8Array(event.data);
            console.log(arraybuffer);
            let new_message = TrainState.decode(arraybuffer);
            console.log(new_message);

            new_message.finished =  ! new_message.finished;
            new_message.loss = Math.random();
            new_message.timestamp = date.getTime()/1000;
            console.log(new_message);
            buffer = TrainState.encode(new_message).finish();
            socket.send(buffer);
        };

        socket.onclose = function (event) {
            if (event.wasClean) {
                alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
            } else {
                // 例如服务器进程被杀死或网络中断
                // 在这种情况下，event.code 通常为 1006
                alert('[close] Connection died');
            }
        };

        socket.onerror = function (error: any) {
            alert(`[error] ${error.message}`);
        };


    }, (err: any) => {
        throw err;
    })

}
