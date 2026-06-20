import { WS_PORT, SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_GRAY, COLOR_BLACK } from './constants.js';
import { Renderer }        from './renderer.js';
import { HUD }             from './hud.js';
import { Menu }            from './menu.js';
import { GameOverScreen }  from './game_over_screen.js';

const canvas = document.getElementById('game');
const ctx    = canvas.getContext('2d');

const renderer       = new Renderer(ctx);
const hud            = new HUD(ctx);
const menu           = new Menu(ctx);
const gameOverScreen = new GameOverScreen(ctx);

let state = null;
let ws    = null;

function connect() {
    ws = new WebSocket(`ws://localhost:${WS_PORT}`);
    ws.onmessage = e => { state = JSON.parse(e.data); };
    ws.onclose   = () => setTimeout(connect, 2000);
    ws.onerror   = () => ws.close();
}

function render() {
    if (!state) {
        ctx.fillStyle = COLOR_BLACK;
        ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
        ctx.fillStyle = COLOR_GRAY;
        ctx.font      = '28px monospace';
        ctx.textAlign = 'center';
        ctx.fillText('Conectando...', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2);
    } else if (state.status === 'MENU') {
        menu.drawMain();
    } else if (state.status === 'MODE_SELECTION') {
        menu.drawModeSelection();
    } else if (state.status === 'PLAYING') {
        renderer.drawGame(state);
    } else if (state.status === 'PAUSED') {
        renderer.drawGame(state);
        hud.drawPause();
    } else if (state.status === 'GAME_OVER') {
        renderer.drawGame(state);
        gameOverScreen.draw(state.winner);
    }
    requestAnimationFrame(render);
}

window.addEventListener('keydown', e => {
    e.preventDefault();
    if (ws?.readyState === WebSocket.OPEN)
        ws.send(JSON.stringify({ type: 'keydown', code: e.code }));
});

window.addEventListener('keyup', e => {
    if (ws?.readyState === WebSocket.OPEN)
        ws.send(JSON.stringify({ type: 'keyup', code: e.code }));
});

connect();
requestAnimationFrame(render);
