import { COLOR_YELLOW, COLOR_WHITE, COLOR_GRAY, SCREEN_WIDTH, SCREEN_HEIGHT } from './constants.js';

export class GameOverScreen {
    constructor(ctx) { this._ctx = ctx; }

    draw(winner) {
        const ctx = this._ctx;
        const cx = SCREEN_WIDTH / 2, cy = SCREEN_HEIGHT / 2;
        ctx.fillStyle = 'rgba(0,0,0,0.6)';
        ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
        ctx.textAlign = 'center';
        ctx.fillStyle = COLOR_YELLOW;
        ctx.font      = 'bold 64px monospace';
        ctx.fillText(`¡${winner} gana!`, cx, cy - 60);
        ctx.fillStyle = COLOR_WHITE;
        ctx.font      = '30px monospace';
        ctx.fillText('[ R ]  Reiniciar', cx, cy + 20);
        ctx.fillStyle = COLOR_GRAY;
        ctx.fillText('[ ESC ]  Menú', cx, cy + 70);
    }
}
