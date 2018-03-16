import * as $ from "jquery";
//import * as io from "socket.io-client";
import * as io from "socket.io-client";

export class Play {
    private socket;
    private self;

    constructor() {
        this.socket = io.connect('http://' + document.domain + ':' + location.port + '/play');

        this.socket.on('connect', () => {
            this.on_connect();
        });
        this.socket.on('refresh', () => {
            this.on_refresh();
        });
    }

    run() {
        let text = <HTMLElement>document.body.querySelector("#text");

        text.addEventListener('keypress', (e) => {
            var code = e.keyCode || e.which;
            if (code == 13) {
                var inp = text.value;
                text.value = '';
                this.socket.emit('client_text', {text: inp});
            }
        }
    }

    on_connect() {
        this.socket.emit('client_connected', {});
    }

    on_refresh() {
        $.ajax({
            url: "/messages",
            type: "get",
            success: function(response: string) {
                $("#message-box").html(response);
            },
            error: function(xhr: string) {
                console.log(xhr);
            }
        }).done(function () {
            $('#message-box').scrollTop($('#message-box')[0].scrollHeight);
        });           
    }

    on_send() {
        console.log("HEYOOOOO");
    }

    leave_room() {
        this.socket.emit('left', {}, () => {
            this.socket.disconnect();
            window.location.href = '/leave_room';
        });
    }
}