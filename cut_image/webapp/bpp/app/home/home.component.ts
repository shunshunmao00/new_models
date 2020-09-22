import {Component, OnInit} from '@angular/core';
import {ModelClient} from '../shared';
import {v4 as uuid} from 'uuid';
import {FileUploader} from 'ng2-file-upload';
import {FileItem} from 'ng2-file-upload/file-upload/file-item.class';

@Component({
    templateUrl: './home.component.html',
})
export class HomeComponent implements OnInit {

    urlModel = '';
    urlFile = '';
    urlWebsocket = '';
    modelUuid = '';
    wsTopic: string;

    websocket: WebSocket;
    tempResults = [];
    results = [];
    // style = 'fire';
    // scale = false;
    // scale_step = 5;
    // word: string;
    error: boolean;
    sending = false;

    fileSelector: FileUploader;
    selectedImgDataUrl: string;
    result: string;

    constructor(
        private modelClient: ModelClient,
    ) {
    }

    ngOnInit() {

        // ******************************************************************************************
        // ***** 请勿修改下面代码段!!! ******************************************************************
        // ******************************************************************************************
        let pathname = window.location.pathname;
        pathname = pathname.replace(/(.*)\//, '$1');  // 先将路径名中最后一个'/'去掉
        let pathnameModel = '';
        let pathnameFile = '';
        let pathnameWebsocket = '';
        if (pathname.lastIndexOf('/web') + 4 === pathname.length) {  // '/web/'出现在最后
            pathnameModel = pathname.replace(/(.*)\/web/, '$1/api/model');  // 再将最后的'/web'替换成'/api/model'
            pathnameFile = pathname.replace(/(.*)\/web/, '$1/api/file/');  // 再将最后的'/web'替换成'/api/file/'
            pathnameWebsocket = pathname.replace(/(.*)\/web/, '$1/websocket');  // 再将最后的'/web'替换成'/api/websocket'
        } else {  // '/web/'出现在中间，用ability做网关的情况下
            pathnameModel = pathname.replace(/(.*)\/web\//, '$1/model/');  // 再将中间的最后一个'/web/'替换成'/model/'
            pathnameFile = pathname.replace(/(.*)\/web\//, '$1/file/') + '/';  // 再将中间的最后一个'/web/'替换成'/file/'，最后再补上'/'
            this.modelUuid = pathname.substring(pathname.lastIndexOf('/') + 1);
        }
        console.log('pathname', pathname);
        console.log('pathnameModel', pathnameModel);
        this.urlModel = window.location.protocol + '//' + window.location.host + pathnameModel;
        this.urlFile = window.location.protocol + '//' + window.location.host + pathnameFile;
        this.urlWebsocket = window.location.protocol + '//' + window.location.host + '/websocket';

        if (this.urlWebsocket.startsWith('http://')) {
            this.urlWebsocket = this.urlWebsocket.replace(/http/, 'ws');
        } else if (this.urlWebsocket.startsWith('https://')) {
            this.urlWebsocket = this.urlWebsocket.replace(/https/, 'wss');
        }

        console.log('urlWebsocket', this.urlWebsocket);
        // ******************************************************************************************
        // ******************************************************************************************

        this.connectWebSocket();

        this.fileSelector = new FileUploader({
            url: this.urlFile + 'classify_bin',
            method: 'POST',
            itemAlias: 'classify_bin',
        });

        this.fileSelector.onAfterAddingFile = (fileItem) => {
            if (this.fileSelector.queue.length > 1) {
                this.fileSelector.queue[0].remove();
            }
            this.readImgFile(fileItem._file);
            // this.uploadFile(fileItem);

        };
    }

    connectWebSocket() {
        if (this.websocket != null) {
            this.websocket.close();
        }

        this.websocket = new WebSocket(this.urlWebsocket);
        this.wsTopic = 'ws_' + uuid();
        const that = this;
        this.websocket.onopen = () => {
            that.websocket.send(JSON.stringify({
                'type': 'subscribe',
                'content': this.wsTopic,
            }));
            that.websocket.send(JSON.stringify({
                'type': 'subscribe_gif2png',
                'topic': 'ability',
                'receiver': this.modelUuid,
                'content': this.wsTopic,
            }));
        };
        this.websocket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            if (message['type'] === 'data') {
                that.tempResults.push(message['content']);
            }
        };
    }

    uploadFile(fileItem: FileItem) {
        fileItem.onSuccess = (response, status, headers) => {
            if (status === 200) {
                const result = JSON.parse(response);
                if (result['status'] === 'ok') {
                    this.result = '识别结果：' + result['value'] + '';
                } else {
                    this.result = '出错啦：' + result['value'];
                }
            } else {
                this.result = '出错啦：' + response;
            }
            this.sending = false;
        };

        fileItem.onError = (response, status, headers) => {
            this.result = '出错啦：' + response;
            this.sending = false;
        };

        this.result = null;
        this.sending = true;
        fileItem.upload();
    }

    readImgFile(file: File) {
        const fileReader = new FileReader();
        fileReader.readAsDataURL(file);
        fileReader.onload = () => {
            this.selectedImgDataUrl = fileReader.result;
            // this.classify();
        };
    }

    genTestImage() {
        this.result = null;
        this.sending = true;
        this.modelClient.access(this.urlModel, 'gen_test_img_base64', {}).subscribe(
            (res) => {
                if (res.body['status'] === 'ok') {
                    this.selectedImgDataUrl = 'data:image/gif;base64,' + res.body['value'];
                    this.sending = false;
                } else {
                    this.result = '出错啦：' + res.body['value'];
                    this.sending = false;
                }
            }
        );
    }

    do_cut() {
        this.results = [];
        this.tempResults = [];
        this.sending = true;
        this.error = false;
        this.modelClient.access(this.urlModel, 'cut_image_base64', {
            'img_base64': this.selectedImgDataUrl,
            'ws_topic': this.wsTopic,
        }).subscribe(
            (res) => {
                if (res.body['status'] === 'ok') {
                    this.results = res.body['value'];
                } else {
                    this.error = true;
                }
                this.sending = false;
            }, (err) => {
                this.error = true;
                this.sending = false;
            }
        );
    }

}
