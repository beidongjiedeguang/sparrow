import {MultiFile, SingleFile} from './interface'
import * as protobuf from 'protobufjs';
// let uniqueFile: SingleFile;
let dataRes: any;
// let filenameList: string[] = [];

const uploadClipElement = document.getElementById('input-clip') as HTMLInputElement;
const downloadClipElement = document.getElementById('download-clip') as HTMLInputElement;
downloadClipElement.onclick = () => {
    download(dataRes.name, dataRes.data, dataRes.type);
}
// add_event_listener()
uploadClipElement.addEventListener('change', clipUpload, false);
let socket = new WebSocket("ws://localhost:8000/ws");
socket.binaryType = 'arraybuffer';


function clipUpload() {
    read_data(uploadClipElement.files!).then((res) => {
        console.log(res);
        dataRes = res;
        protobuf.load('./proto/sparray.proto').then((root: any) => {
            let Sparray = root.lookupType("sparray.DocProto");
            const payload = {
                'id': '1',
                'blob': new Uint8Array(dataRes['data']),
                // 'text': dataRes['name']
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

    })
}


function read_data(files: HTMLInputElement['files']) {
    // return files;
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
