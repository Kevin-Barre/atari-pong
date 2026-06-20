# Atari Pong — Versión Personalizada

Proyecto universitario — Universidad Internacional del Ecuador  
Materia: Arquitectura de Software  
Autor: Kevin Barré Espín · Quito, Mayo 2026

Reimplementación del Pong clásico usando una arquitectura híbrida: **Python** ejecuta la lógica del juego, **HTML5 Canvas** renderiza en el navegador, y **WebSocket** los conecta en tiempo real. Arquitectura limpia en 4 capas con principios SOLID.

---

## Mecánicas base

| Pregunta | Decisión de diseño |
|---|---|
| Movimiento de la pelota | Vectores de velocidad X/Y que se modifican al colisionar |
| Detección de colisiones | AABB — Axis-Aligned Bounding Boxes |
| Inteligencia artificial | Sigue la posición Y de la pelota con velocidad limitada (vencible) |
| Fin de partida | Primer jugador que alcanza **5 puntos** |
| Controles 2 jugadores | Jugador 1: `W` / `S` — Jugador 2: `↑` / `↓` |

---

## Funcionalidades nuevas (no existen en el Pong original)

| # | Feature | Descripción |
|---|---|---|
| 1 | **Velocidad incremental** | La pelota aumenta su velocidad un **5 %** con cada rebote en paleta |
| 2 | **Sistema de power-ups** | Aparecen aleatoriamente en el campo; hacen **crecer o encoger** la paleta del jugador que los recoge |
| 3 | **Modo 2 jugadores local** | Mismo teclado, controles diferenciados por jugador |
| 4 | **Ángulo de rebote variable** | El ángulo de salida depende de la **zona de impacto** en la paleta |

---

## Diagramas

### 2.1 Diagrama de casos de uso

![Diagrama de casos de uso](assets/digrama-casos-uso-1.png)

---

### 2.2 Diagrama de flujo — Ciclo principal del juego (60 FPS)

![Diagrama de flujo - ciclo principal](assets/diagrama-flujo-2.png)

---

### 2.3 Diagrama de flujo — Colisiones de la pelota

![Diagrama de flujo - colisiones](assets/diagrma-flujo-colisiones-3.png)

---

### 2.4 Diagrama de actividad — Estados del juego

![Diagrama de actividad - estados](assets/diagrma-actividad-4.png)

---

### 3. Diagrama de arquitectura en capas

![Diagrama de arquitectura en capas](assets/diagrama-arquitectura-5.png)

> Las capas solo dependen hacia abajo. La Capa 4 no importa nada del resto del sistema.

---

## Arquitectura

```
Python backend (logic + engine + state)
        ↕  WebSocket (JSON, ~60 FPS)
HTML5 Canvas frontend (presentation)
```

| Capa | Tecnología | Responsabilidad |
|---|---|---|
| Presentación | HTML5 Canvas + JavaScript | Renderiza el juego en el navegador |
| Motor | Python asyncio + websockets | Loop 60 FPS, orquesta todo, sirve el frontend |
| Lógica | Python | Física, colisiones AABB, IA, power-ups |
| Estado | Python dataclasses | Datos puros, sin lógica |

## Requisitos

```
Python >= 3.9
websockets >= 12.0
```

## Instalación y ejecución

```bash
pip install websockets
python main.py
# Abre automáticamente http://localhost:8080 en el navegador
```

## Controles

| Acción | Jugador 1 | Jugador 2 |
|---|---|---|
| Mover arriba | `W` | `↑` |
| Mover abajo | `S` | `↓` |
| Pausar | `P` | `P` |
| Reiniciar (game over) | `R` | `R` |
| Salir | `ESC` | `ESC` |
