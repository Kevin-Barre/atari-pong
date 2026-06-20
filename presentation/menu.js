import { COLOR_BLACK, COLOR_WHITE, COLOR_GRAY,
         COLOR_CYAN, COLOR_GREEN, SCREEN_WIDTH, SCREEN_HEIGHT } from './constants.js';

export class Menu {
    constructor(ctx) { this._ctx = ctx; }

    drawMain() {
        const ctx = this._ctx;
        const cx = SCREEN_WIDTH / 2, cy = SCREEN_HEIGHT / 2;
        ctx.fillStyle = COLOR_BLACK;
        ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
        ctx.textAlign = 'center';
        ctx.fillStyle = COLOR_WHITE;
        ctx.font      = 'bold 80px monospace';
        ctx.fillText('ATARI PONG', cx, cy - 60);
        ctx.fillStyle = COLOR_GRAY;
        ctx.font      = '30px monospace';
        ctx.fillText('[ ENTER ]  Jugar', cx, cy + 20);
        ctx.font      = '18px monospace';
        ctx.fillText('Universidad Internacional del Ecuador', cx, cy + 130);
    }

    drawModeSelection() {
        const ctx = this._ctx;
        const cx = SCREEN_WIDTH / 2, cy = SCREEN_HEIGHT / 2;
        ctx.fillStyle = COLOR_BLACK;
        ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
        ctx.textAlign = 'center';
        ctx.fillStyle = COLOR_WHITE;
        ctx.font      = 'bold 56px monospace';
        ctx.fillText('MODO DE JUEGO', cx, cy - 80);
        ctx.fillStyle = COLOR_CYAN;
        ctx.font      = '32px monospace';
        ctx.fillText('[ 1 ]  1 Jugador  (vs IA)', cx, cy);
        ctx.fillStyle = COLOR_GREEN;
        ctx.fillText('[ 2 ]  2 Jugadores', cx, cy + 55);
        ctx.fillStyle = COLOR_GRAY;
        ctx.font      = '22px monospace';
        ctx.fillText('[ ESC ]  volver', cx, cy + 115);
    }
}
