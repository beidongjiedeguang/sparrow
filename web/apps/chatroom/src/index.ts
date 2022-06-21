import * as protobuf from 'protobufjs';

let socket = new WebSocket("ws://localhost:8000/ws_chat");
socket.binaryType = 'arraybuffer'

let btn = document.getElementById('btn') as HTMLElement
const uploadClipElement = document.getElementById('sendFile') as HTMLInputElement;
let chatRoom = document.getElementById('chatRoom')
const context = document.getElementById('context') as any;
const contextUserName = document.getElementById('uName') as any;
let ChatProto: any;

func2()
uploadClipElement.addEventListener('change', clipUpload, false);

function clipUpload() {
    // preview_image(uploadClipElement.files!).then(res=>{
    //         imgElement.src = res;
    // });

    read_data(uploadClipElement.files!).then((res) => {
        console.log("here");
        console.log(res);
        let dataRes = res as any;
        const payload = {
            'msg': dataRes['msg'],
            'buffer': new Uint8Array(dataRes['buffer']),
            'name': dataRes['name'],
            'dtype': dataRes['dtype']
        };
        console.log(dataRes);

        let errMsg = ChatProto.verify(payload);
        if (errMsg) {
            throw Error(errMsg);
        }
        const message = ChatProto.create(payload);
        console.log(message);
        const buffer = ChatProto.encode(message).finish();
        socket.send(buffer);

        })
    }



function func2() {
    // const date = new Date();
    protobuf.load('./proto/sparray.proto').then((root: any) => {
        ChatProto = root.lookupType("sparray.ChatProto");
        let payload = {
            "name": "you",
            "msg": "hello websocket"
        };
        let errMsg = ChatProto.verify(payload);
        if (errMsg) {
            throw Error(errMsg);
        }
        let message = ChatProto.create(payload);
        console.log(message);

        console.log(`message = ${JSON.stringify(message)}`);

        let buffer = ChatProto.encode(message).finish();

        socket.onopen = (e: Event) => {
            socket.send(buffer);
        };

    btn.onclick = function() {
        const new_message = ChatProto.decode(buffer);
        new_message.msg = context.value;
        new_message.name = contextUserName.value;
        buffer = ChatProto.encode(new_message).finish();
        socket.send(buffer);
    }

    socket.onmessage = async (event: MessageEvent) => {
        let arraybuffer = new Uint8Array(event.data);
        const new_message = ChatProto.decode(arraybuffer);

        console.log("接收到从python发来的数据：\n", new_message);
        // new_message.time = date.getTime() / 1000;
        chatRoom!.innerHTML += `<div>${new_message.name}: ${new_message.msg} </div>`;
        console.log(new_message.buffer.length);
        // if (new_message.buffer.length !== 0){
        //     let imgEle = document.createElement('img');
        //     const url = arraybuffer2base64(new_message.buffer);
        //     imgEle.src = 'data:image/png;base64,'+url;
        //     imgEle.height = 200

        //     chatRoom!.appendChild(imgEle);
        // }
    };

    socket.onclose = function (event: CloseEvent) {
        if (event.wasClean) {
            alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
        } else {
            alert('[close] Connection died');
        }
    };

    socket.onerror = function (error: any) {
        alert(`[error] ${error.message}`);
    };


},
    (err: any) => {
    throw err;
})

}

function read_data(files: HTMLInputElement['files']) {
    return new Promise((resolve, reject) => {
        for (let i = 0; i < files!.length; i++) {
            let item = files!.item(i)!;
            console.log("item:\n");
            console.log(item);

            const fileReader = new FileReader();
            fileReader.readAsArrayBuffer(item!);
            fileReader.onload = (evt) => {
                console.log("event:\n");
                console.log(evt);
                resolve({
                    "msg": "file",
                    "buffer": evt.target!.result,
                    "dtype": item.type,
                    "name": item.name
                });
            }
        }
    });
}

function arraybuffer2base64(arraybuffer: Uint8Array){
    let binary = '';
    // let bytes = new Uint8Array(arraybuffer);
    let bytes = arraybuffer;
    for (let i =0; i < bytes.length; i++){
        binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
}

async function chunkedUpload(file: File, chunkSize: number, url: string) {
    for (let start = 0; start < file.size; start += chunkSize) {
        const chunk = file.slice(start, start + chunkSize + 1)
        const fd = new FormData()
        fd.append('data', chunk)
        await fetch(url, {method: 'post', body: fd}).then(
            (res) => res.text()).then(
                res => {
                    console.log(res)
        })
    }
}

// const file = new File(['a'.repeat(1000000)], 'test.txt')
// const chunkSize = 40000
// const url = 'https://httpbin.org/post'
// chunkedUpload(file, chunkSize, url)