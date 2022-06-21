import * as protobuf from 'protobufjs';


const local = true;

let websocket_dir:string;
if (local){
    websocket_dir = "ws://0.0.0.0:8000/ws_chat"
}else{
    websocket_dir = "ws://192.168.61.230:51221/ws_chat"
}
let socket = new WebSocket(websocket_dir);
socket.binaryType = 'arraybuffer'

let btn = document.getElementById('btn') as HTMLElement
const uploadClipElement = document.getElementById('sendFile') as HTMLInputElement;
let chatRoom = document.getElementById('chatRoom')
const context = document.getElementById('context') as any;
const contextUserName = document.getElementById('uName') as any;
let ChatProto: any;
let hello_buffer: any;
let imageWidth: number = 0;
let imageHeight: number = 0;

func2()

uploadClipElement.addEventListener('change', clipUpload, false);

function clipUpload() {


    read_data(uploadClipElement.files!).then(async (res) => {
        console.log(res);
        let dataRes = res as any;
        if (dataRes['dtype'].startsWith("image")){
        await read_img_data(uploadClipElement.files!).then((imgInfo: any) => {
            console.log(imgInfo);
            imageWidth = imgInfo!['width'];
            imageHeight = imgInfo!['height'];
        });
    }
        const payload = {
            'msg': dataRes['msg'],
            'buffer': new Uint8Array(dataRes['buffer']),
            'name': dataRes['name'],
            'dtype': dataRes['dtype'],
            'imgInfo': {'width': imageWidth, 'height': imageHeight}
        };
        let errMsg = ChatProto.verify(payload);
        if (errMsg) {
            throw Error(errMsg);
        }
        const message = ChatProto.create(payload);
        console.log(message);
        const buffer = ChatProto.encode(message).finish();
        socket.send(buffer);
    });

    }


function func2() {
    // const date = new Date();
    protobuf.load('./proto/sparray.proto').then((root: any) => {
    ChatProto = root.lookupType("sparray.ChatProto");
    let payload = {
        "name": "kunyuan",
        "msg": "Hello 欢迎来到我的聊天室"
    };
    let errMsg = ChatProto.verify(payload);
    if (errMsg) {
        throw Error(errMsg);
    }
    let message = ChatProto.create(payload);
    console.log(message);

    console.log(`message = ${JSON.stringify(message)}`);

    hello_buffer = ChatProto.encode(message).finish();
    socket.onopen = (e: Event) => {
            socket.send(hello_buffer);
        };
},
    (err: any) => {
    throw err;
})

}


    btn.onclick = function() {
        const new_message = ChatProto.decode(hello_buffer);
        new_message.msg = context.value;
        new_message.name = contextUserName.value;
        hello_buffer = ChatProto.encode(new_message).finish();
        socket.send(hello_buffer);
    }

    socket.onmessage = async (event: MessageEvent) => {
        let arraybuffer = new Uint8Array(event.data);
        const new_message = ChatProto.decode(arraybuffer);

        console.log("接收到从python发来的数据：\n", new_message);
        // new_message.time = date.getTime() / 1000;
        chatRoom!.innerHTML += `<div>${new_message.name}: ${new_message.msg} </div>`;
        if (new_message.buffer.length !== 0){
            const url = arraybuffer2base64(new_message.buffer);
            // let imgEle = document.createElement('img');
            // imgEle.src = 'data:image/png;base64,'+url;
            // imgEle.width = 500
            // chatRoom!.appendChild(imgEle);
            let image = new Image();
            image.src = 'data:image/png;base64,'+url;
            const imgInfo = new_message.imgInfo
            if (imgInfo.width / imgInfo.height > 1){
                image.width = 300;
            }else{
                image.height = 300;
            }


            chatRoom!.appendChild(image);
        }
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



async function read_img_data(files: HTMLInputElement['files']){

    return new Promise((resolve, reject) => {
        for (let i = 0; i < files!.length; i++) {
            let item = files!.item(i)!;
            const imgFileReader = new FileReader();
            imgFileReader.readAsDataURL(item!);
            let image = new Image() as any;
            imgFileReader.onload = (evt) => {
                console.log("event:\n");
                console.log(evt);
                image.onload = ()=>{
                    imageWidth = image.width;
                    imageHeight = image.height;
                    resolve({'width': image.width, 'height': image.height});
                };
                image.src = evt.target!.result;
            }
        }
    })
}

function read_data(files: HTMLInputElement['files']) {
    return new Promise((resolve, reject) => {
        for (let i = 0; i < files!.length; i++) {
            let item = files!.item(i)!;
            console.log("item:\n");
            console.log(item);

            const fileReader = new FileReader();
            fileReader.readAsArrayBuffer(item);
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