from __future__ import annotations
import asyncio
import json
import webbrowser
from pathlib import Path

import websockets
import websockets.exceptions

import constants
from engine.game_loop import GameLoop

game    = GameLoop()
clients: set = set()


async def ws_handler(websocket) -> None:
    clients.add(websocket)
    try:
        async for raw in websocket:
            event = json.loads(raw)
            if event["type"] == "keydown":
                game.on_key_down(event["code"])
            elif event["type"] == "keyup":
                game.on_key_up(event["code"])
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clients.discard(websocket)


async def game_runner() -> None:
    target_dt = 1.0 / constants.FPS
    loop = asyncio.get_event_loop()
    while True:
        t0 = loop.time()
        game.update(target_dt)
        if clients:
            payload = json.dumps(game.to_dict())
            await asyncio.gather(
                *[ws.send(payload) for ws in list(clients)],
                return_exceptions=True,
            )
        elapsed = loop.time() - t0
        await asyncio.sleep(max(0.0, target_dt - elapsed))


async def main() -> None:
    html = Path(__file__).parent / "presentation" / "index.html"
    url  = html.as_uri()
    print(f"Servidor WebSocket corriendo en ws://localhost:{constants.WS_PORT}")
    print(f"Abriendo juego en: {url}")
    webbrowser.open(url)
    async with websockets.serve(ws_handler, "localhost", constants.WS_PORT):
        await game_runner()


if __name__ == "__main__":
    asyncio.run(main())
