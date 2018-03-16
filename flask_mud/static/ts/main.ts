import * as jquery from 'jquery';
import "../sass/main.scss";
import {Play} from "./play"

window.$ = jquery;
window.play = new Play();

window.onload = () => {
    console.log("Window loaded.");
}