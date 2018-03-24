import * as $ from "jquery";
//import * as io from "socket.io-client";
import * as io from "socket.io-client";

export class Play {
    private socket;
    private self;

    constructor() {
        this.socket = io.connect('http://' + document.domain + ':' + location.port + '/play', {'sync disconnect on unload': true});

        this.socket.on('connect', () => {
            this.on_connect();
        });
        this.socket.on('refresh', () => {
            this.on_refresh();
        });
        this.socket.on('player_change', () => {
            this.on_player_change();
        });
    }

    run() {
        let text = <HTMLElement>document.body.querySelector("#text");

        $('#text-editor-submit').click(() => {
            var inp = $('#text-editor-area').val;
            $('#text-editor-area').val = '';
            this.socket.emit('client_text', {text: inp});
        });

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
        console.log("refreshed");
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
            $("html, body").animate({ scrollTop: $(document).height()-$(window).height() });
            //$('#message-box').scrollTop($('#message-box')[0].scrollHeight);
        });           
    }

    on_player_change() {
        console.log("players changed");
        $.ajax({
            url: "/get_players",
            type: "get",
            success: function(response: string) {
                $("#player-list").html(response);
            },
            error: function(xhr: string) {
                console.log(xhr);
            }
        });
    }

    on_send() {
        console.log("HEYOOOOO");
    }

    on_text_editor_submit() {
        let text = <HTMLElement>document.body.querySelector("#text-editor-area");

        var inp = text.value;
        text.value = '';
        this.socket.emit('client_text', {text: inp});
    }

    leave_room() {
        this.socket.emit('left', {}, () => {
            this.socket.disconnect();
            window.location.href = '/leave_room';
        });
    }
}