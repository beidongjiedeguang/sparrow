import * as protobuf from 'protobufjs';

let socket = new WebSocket("ws://localhost:8000/ws_chat");
socket.binaryType = 'arraybuffer'

// // 文本框内容
// // 点击按钮
let btn = document.getElementById('btn') as HTMLElement
// 要显示聊天室的区域
let chatRoom = document.getElementById('chatRoom')

let chat_context: any;



func2()


function func2() {
    const date = new Date();

    protobuf.load('./proto/sparray.proto').then((root: any) => {

        let ChatProto = root.lookupType("sparray.ChatProto");
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
    const context = document.getElementById('context') as any;
    const contextUserName = document.getElementById('uName') as any;

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
            // chatRoom!.innerHTML +=  `<strong>${JSON.stringify(new_message.msg)}</strong>`;
        };

        socket.onclose = function (event: CloseEvent) {
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


    },
        (err: any) => {
        throw err;
    })

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