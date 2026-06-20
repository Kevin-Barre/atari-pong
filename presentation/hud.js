import { COLOR_WHITE, COLOR_GRAY, SCREEN_WIDTH, SCREEN_HEIGHT } from './constants.js';

export class HUD {
    constructor(ctx) { this._ctx = ctx; }

    drawPause() {
        const ctx = this._ctx;
        ctx.fillStyle = 'rgba(0,0,0,0.55)';
        ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
        ctx.textAlign = 'center';
        ctx.fillStyle = COLOR_WHITE;
        ctx.font      = 'bold 56px monospace';
        ctx.fillText('PAUSA', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20);
        ctx.fillStyle = COLOR_GRAY;
        ctx.font      = '28px monospace';
        ctx.fillText('[ P ]  continuar', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 32);
    }
}
