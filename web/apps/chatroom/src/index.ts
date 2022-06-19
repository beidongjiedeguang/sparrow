import * as protobuf from 'protobufjs';

let socket = new WebSocket("ws://localhost:8000/ws_chat");
socket.binaryType = 'arraybuffer'

// // 文本框内容
// // 点击按钮
let btn = document.getElementById('btn') as HTMLElement
// 要显示聊天室的区域
let charRoom = document.getElementById('charRoom')

let chat_context: any;



func2()


function func2() {
    const date = new Date();

    protobuf.load('./proto/trainstatus.proto').then((root: any) => {

        let TrainState = root.lookupType("protostatus.TrainStatus");
        let payload = {
            "loss": 0.1,
            "step": 100,
            "progress": 0.99,
            "finished": false,
            "cost_time": date.getTime() / 1000,
            "msg": "hello websocket"
        };
        let errMsg = TrainState.verify(payload);
        if (errMsg) {
            throw Error(errMsg);
        }
        let message = TrainState.create(payload);
        console.log(message);
        console.log(`message = ${JSON.stringify(message)}`);

        let buffer = TrainState.encode(message).finish();

        socket.onopen = (e: Event) => {
            socket.send(buffer);
        };
    const context = document.getElementById('context') as any;

    btn.onclick = function() {
        // const hello = "Hello world"
        // charRoom!.innerHTML += `
        // <strong>${hello}</strong>
        // `
        // console.log("emmmmmmmmmmmmmm");
        console.log(context.value);
        chat_context = context.value;
        const new_message = TrainState.decode(buffer);
        new_message.msg = context.value;
        buffer = TrainState.encode(new_message).finish();
        socket.send(buffer);
    }
        // socket.onmessage = async (event: MessageEvent) => {
        //     alert(`[message] Data received from server: ${event.data}`);
        //     let arraybuffer = new Uint8Array(event.data);
        //     const new_message = TrainState.decode(arraybuffer);

        //     console.log("接收到从python发来的数据：\n", new_message);

        //     new_message.finished = !new_message.finished;
        //     new_message.loss = Math.random();
        //     new_message.time = date.getTime() / 1000;
        //     console.log("发送给python的数据: \n", new_message);
        //     buffer = TrainState.encode(new_message).finish();
        //     socket.send(buffer);

        //     const messages = document.getElementById('messages')
        //     let message = document.createElement('ele_one')
        //     let content = document.createTextNode(event.data)
        //     message.appendChild(content)
        //     messages!.appendChild(message)
        // };

        socket.onmessage = async (event: MessageEvent) => {
            // alert(`[message] Data received from server: ${event.data}`);
            let arraybuffer = new Uint8Array(event.data);
            const new_message = TrainState.decode(arraybuffer);

            console.log("接收到从python发来的数据：\n", new_message);

            // new_message.finished = !new_message.finished;
            // new_message.loss = Math.random();
            // new_message.time = date.getTime() / 1000;
            new_message.time = 100;
            console.log("发送给python的数据: \n", new_message);
            buffer = TrainState.encode(new_message).finish();
            // socket.send(buffer);

            // 添加到页面上
            charRoom!.innerHTML += `
                <strong>${JSON.stringify(new_message)}：</strong>
            `
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