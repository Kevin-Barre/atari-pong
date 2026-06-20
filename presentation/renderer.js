import { COLOR_BLACK, COLOR_WHITE, COLOR_GRAY, COLOR_GREEN,
         COLOR_RED, COLOR_YELLOW, SCREEN_WIDTH, SCREEN_HEIGHT } from './constants.js';

export class Renderer {
    constructor(ctx) { this._ctx = ctx; }

    drawGame(state) {
        this._ctx.fillStyle = COLOR_BLACK;
        this._ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
        this._drawCenterLine();
        this._drawPaddle(state.paddleLeft);
        this._drawPaddle(state.paddleRight);
        this._drawBall(state.ball);
        if (state.powerUp) this._drawPowerUp(state.powerUp);
        this._drawScores(state);
        this._drawEffectTimers(state);
    }

    _drawCenterLine() {
        this._ctx.fillStyle = COLOR_GRAY;
        for (let y = 10; y < SCREEN_HEIGHT; y += 30)
            this._ctx.fillRect(SCREEN_WIDTH / 2 - 2, y, 4, 16);
    }

    _drawPaddle(p) {
        const ctx = this._ctx, r = 4;
        ctx.fillStyle = COLOR_WHITE;
        ctx.beginPath();
        ctx.moveTo(p.x + r, p.y);
        ctx.arcTo(p.x + p.width, p.y,            p.x + p.width, p.y + p.height, r);
        ctx.arcTo(p.x + p.width, p.y + p.height, p.x,           p.y + p.height, r);
        ctx.arcTo(p.x,           p.y + p.height, p.x,           p.y,            r);
        ctx.arcTo(p.x,           p.y,            p.x + p.width, p.y,            r);
        ctx.closePath();
        ctx.fill();
    }

    _drawBall(ball) {
        const ctx = this._ctx;
        ctx.fillStyle = COLOR_WHITE;
        ctx.beginPath();
        ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
        ctx.fill();
    }

    _drawPowerUp(pu) {
        const ctx = this._ctx;
        ctx.fillStyle   = pu.type === 'GROW' ? COLOR_GREEN : COLOR_RED;
        ctx.strokeStyle = COLOR_WHITE;
        ctx.lineWidth   = 2;
        ctx.beginPath();
        ctx.arc(pu.x, pu.y, pu.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
    }

    _drawScores(state) {
        const ctx = this._ctx;
        ctx.fillStyle = COLOR_WHITE;
        ctx.font      = 'bold 64px monospace';
        ctx.textAlign = 'center';
        ctx.fillText(state.scoreLeft,  SCREEN_WIDTH / 4,     70);
        ctx.fillText(state.scoreRight, SCREEN_WIDTH * 3 / 4, 70);
    }

    _drawEffectTimers(state) {
        const ctx = this._ctx;
        ctx.font = '22px monospace';
        if (state.effectTimerLeft > 0) {
            ctx.fillStyle = COLOR_YELLOW;
            ctx.textAlign = 'left';
            ctx.fillText(`P1  ${Math.ceil(state.effectTimerLeft)}s`, 10, SCREEN_HEIGHT - 14);
        }
        if (state.effectTimerRight > 0) {
            ctx.fillStyle = COLOR_YELLOW;
            ctx.textAlign = 'right';
            ctx.fillText(`P2  ${Math.ceil(state.effectTimerRight)}s`, SCREEN_WIDTH - 10, SCREEN_HEIGHT - 14);
        }
    }
}
