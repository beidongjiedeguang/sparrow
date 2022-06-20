import {MultiFile, SingleFile} from './interface'
import * as protobuf from 'protobufjs';
// let uniqueFile: SingleFile;
let dataRes: any;
// let filenameList: string[] = [];
let Sparray: any;

function arraybuffer2base64(arraybuffer: Uint8Array){
    let binary = '';
    // let bytes = new Uint8Array(arraybuffer);
    let bytes = arraybuffer;
    for (let i =0; i < bytes.length; i++){
        binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
}

protobuf.load('./proto/sparray.proto').then((root: any) => {
    Sparray = root.lookupType("sparray.DocProto");

    const uploadClipElement = document.getElementById('input-clip') as HTMLInputElement;
    const downloadClipElement = document.getElementById('download-clip') as HTMLInputElement;
    const imgElement = document.getElementById("image_preview") as any;

    downloadClipElement.onclick = () => {
        download(dataRes.name, dataRes.data, dataRes.type);
    }

    uploadClipElement.addEventListener('change', clipUpload, false);
    let socket = new WebSocket("ws://localhost:8000/ws_tunnel");
    socket.binaryType = 'arraybuffer';

    socket.onmessage = async (event: MessageEvent) => {
            console.log(`[message] Data received from server: ${event.data}`);

            let arraybuffer = new Uint8Array(event.data);
            const new_message = Sparray.decode(arraybuffer) as any;
            console.log("接收到从python发来的数据：\n", new_message);
            // const type = new_message.dtype;
            // const blob = new Blob([new_message.data], {type});
            // console.log(blob);
            const url = arraybuffer2base64(new_message.blob);
            console.log(url)
            imgElement.src = 'data:image/jpeg;base64,'+url;


            // element.setAttribute('href', objUrl);
            // element.setAttribute('download', filename);
            // element.style.display = 'none';
            // document.body.appendChild(element);


            // // new_message.loss = Math.random();
            // // new_message.time = date.getTime() / 1000;
            // // new_message.time = 100;
            // console.log("发送给python的数据: \n", new_message);
            // let buffer = Sparray.encode(new_message).finish();
            // socket.send(buffer);

            // 添加到页面上
            // charRoom!.innerHTML += `
                // <strong>${JSON.stringify(new_message)}：</strong>
            // `
        };



    function clipUpload() {
        // preview_image(uploadClipElement.files!).then(res=>{
        //         imgElement.src = res;
        // });

        read_data(uploadClipElement.files!).then((res) => {
            console.log(res);
            dataRes = res;
            const payload = {
                'id': '1',
                'blob': new Uint8Array(dataRes['data']),
                'text': dataRes['name'],
                'dtype': dataRes['type']
            };
            console.log(dataRes);

            let errMsg = Sparray.verify(payload);
            if (errMsg) {
                throw Error(errMsg);
            }
            const message = Sparray.create(payload);
            console.log(message);
            const buffer = Sparray.encode(message).finish();
            socket.send(buffer);

            })
        }
    })

function preview_image(files: HTMLInputElement['files']){
    return new Promise((resolve, reject) => {
        for (let i = 0; i < files!.length; i++) {
            let item = files!.item(i)!;
            const fileReader = new FileReader();
            fileReader.readAsDataURL(item!);
            fileReader.onload = (evt) => {
                resolve(evt.target!.result);
            }
        }
    });
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
                    "data": evt.target!.result,
                    "type": item.type,
                    "name": item.name
                });
            }
        }
    });
}

/**
 *
 * @param filename
 * @param data object data
 * @param type string
 */
export function download(filename: string, data: any, type: string) {
    const blob = new Blob([data], {type});
    const objUrl = URL.createObjectURL(blob);
    const element = document.createElement('a');
    element.setAttribute('href', objUrl);
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

// 看上去这里的save()和上面的dowload()是一样的......
export function saveArrayBuffer(buffer: any, filename: string) {
    save(new Blob([buffer], {type: 'application/octet-stream'}), filename);
}

export function saveString(text: string, filename: string) {
    save(new Blob([text], {type: 'text/plain'}), filename);
}


function save(blob: any, filename: string) {
    const link = document.createElement('a');
    link.style.display = 'none';
    document.body.appendChild(link);
    link.setAttribute('href', URL.createObjectURL(blob));
    link.setAttribute('download', filename);
    link.click();
    document.body.removeChild(link);
}

const state = {
    upload: {
        url: undefined as any,
    },
    download: {
        jsonFile: undefined as any,
        bufferFile: undefined as any,
        savePath: ''
    }
}
