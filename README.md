# Atari Pong — Versión Personalizada

Proyecto universitario — Universidad Internacional del Ecuador  
Materia: Arquitectura de Software  
Autor: Kevin Barré Espín · Quito, Mayo 2026

Reimplementación del Pong clásico en Python con cuatro funcionalidades propias, siguiendo una arquitectura limpia en capas con principios SOLID.

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

```mermaid
graph LR
    J1(["👤 Jugador 1\n(W / S)"])
    J2(["👤 Jugador 2 / IA\n(↑ / ↓)"])
    SYS(["⚙️ Sistema"])

    subgraph BASE ["Funcionalidad base"]
        UC1([Mover paleta])
        UC2([Seleccionar modo de juego])
        UC3([Pausar / reanudar juego])
        UC4([Ver marcador])
    end

    subgraph FEATURES ["Features propias"]
        UC5([Recoger power-up])
        UC6([Rebote con ángulo variable])
        UC7([Velocidad incremental])
    end

    subgraph AUTO ["Procesos automáticos del sistema"]
        UC8([Detectar colisiones AABB])
        UC9([Calcular movimiento IA])
        UC10([Generar power-ups aleatorios])
        UC11([Gestionar puntaje])
    end

    J1 --> UC1
    J1 --> UC2
    J1 --> UC3
    J1 --> UC5
    J2 --> UC1
    J2 --> UC5
    SYS --> UC8
    SYS --> UC9
    SYS --> UC10
    SYS --> UC11
    SYS --> UC6
    SYS --> UC7
```

---

### 2.2 Diagrama de flujo — Ciclo principal del juego (60 FPS)

```mermaid
flowchart TD
    A([Inicio]) --> B[Inicializar pygame\ny entidades]
    B --> C{Estado del juego}
    C -->|MENU| D[Mostrar pantalla de inicio]
    D --> C
    C -->|MODE_SELECTION| E[Mostrar selección\n1P / 2P]
    E --> C
    C -->|PLAYING| F[Leer entrada Jugador 1\nW / S]
    F --> G[Leer entrada Jugador 2\no calcular IA]
    G --> H[Mover paletas]
    H --> I[Mover pelota]
    I --> J[Verificar colisiones]
    J --> K[Aplicar efectos\nde power-ups]
    K --> L[Dibujar fotograma]
    L --> M{¿Jugador llegó\na 5 puntos?}
    M -->|Sí| N([GAME_OVER])
    M -->|No| O{¿Pausa?}
    O -->|Sí| P[Mostrar pantalla\nde pausa]
    P --> O
    O -->|No| F
    C -->|GAME_OVER| Q[Mostrar ganador\ny opción de reinicio]
    Q --> C
```

---

### 2.3 Diagrama de flujo — Colisiones de la pelota

```mermaid
flowchart TD
    A([Pelota se mueve]) --> B{¿Colisión\ncon paleta?}
    B -->|Sí| C[Invertir dirección X]
    C --> D[Calcular ángulo según\nzona de impacto]
    D --> E[Aumentar velocidad +5%]
    E --> Z([Siguiente frame])

    B -->|No| F{¿Colisión con\nborde superior/inferior?}
    F -->|Sí| G[Invertir dirección Y\nsin cambiar velocidad]
    G --> Z

    F -->|No| H{¿Colisión\ncon power-up?}
    H -->|Sí| I[Aplicar efecto en paleta\ndel jugador más cercano]
    I --> J[Desactivar power-up]
    J --> Z

    H -->|No| K{¿Pelota fuera\ndel campo?}
    K -->|Sí| L[Sumar punto al\njugador contrario]
    L --> M[Reiniciar pelota\ncon velocidad base]
    M --> Z

    K -->|No| Z
```

---

### 2.4 Diagrama de actividad — Estados del juego

```mermaid
stateDiagram-v2
    [*] --> MENU : inicio del programa

    MENU --> MODE_SELECTION : presionar ENTER

    MODE_SELECTION --> PLAYING : elegir 1 Jugador
    MODE_SELECTION --> PLAYING : elegir 2 Jugadores
    MODE_SELECTION --> MENU : presionar ESC

    PLAYING --> PAUSED : presionar P
    PAUSED --> PLAYING : presionar P

    PLAYING --> GAME_OVER : jugador llega a 5 puntos

    GAME_OVER --> MENU : presionar R para reiniciar
    GAME_OVER --> [*] : presionar ESC para salir
```

---

### 3. Diagrama de arquitectura en capas

```mermaid
graph TD
    subgraph L1 ["Capa 1 — Presentación"]
        HUD[HUD: marcador y power-up activo]
        MENU[Menú: inicio y selección de modo]
        GO[Pantalla de fin de partida]
    end

    subgraph L2 ["Capa 2 — Motor del juego"]
        LOOP[GameLoop: ciclo 60 FPS]
        RENDER[Renderer: dibuja cada fotograma]
        INPUT[InputHandler: P1 W/S · P2 flechas]
    end

    subgraph L3 ["Capa 3 — Lógica del juego"]
        PHYS[BallPhysics: velocidad incremental + ángulo]
        COLL[CollisionEngine: AABB]
        SCORE[ScoreManager]
        AI[AIController]
        PWUP[PowerUpManager]
    end

    subgraph L4 ["Capa 4 — Estado del juego (datos puros)"]
        GS[GameState: estado global]
        BALL[Ball: posición + velocidad]
        PAD[Paddle: posición + tamaño]
        PU[PowerUp: tipo + duración]
    end

    L1 -->|lee estado para renderizar| L2
    L2 -->|ejecuta lógica cada frame| L3
    L3 -->|lee y escribe entidades| L4
```

> Las capas solo dependen hacia abajo. La Capa 4 no importa nada del resto del sistema.

---

## Requisitos

```
Python >= 3.11
pygame >= 2.5
```

## Instalación y ejecución

```bash
pip install pygame
python main.py
```

## Controles

| Acción | Jugador 1 | Jugador 2 |
|---|---|---|
| Mover arriba | `W` | `↑` |
| Mover abajo | `S` | `↓` |
| Pausar | `P` | `P` |
| Reiniciar (game over) | `R` | `R` |
| Salir | `ESC` | `ESC` |
