# Brawlers: A Real-Time 2D Fighting Game

## Overview
**Brawlers** is a real-time 2D fighting game developed using Python and Pygame. The game features dynamic combat mechanics, three arenas, and engaging AI. Compete against an AI-controlled opponent, utilizing smooth animations, health tracking, and reactive controls. Developed by Oluwasegun Adewola and Ifeoluwa Areogun. Check out our [Trailer](https://www.youtube.com/watch?v=Z0DYOHhNvm0).

---

## Gameplay Features
- **Real-Time Combat**:
  - Players can attack, jump, and perform special moves.
- **Arenas**:
  - Choose from three visually distinct battlefields before starting the game.
- **Dynamic Health Bars**:
  - Reflect real-time damage and provide visual feedback during combat.
- **AI Opponent**:
  - Adaptive AI with randomized attacks and strategic movements.

---

## How to Play
1. **Select Your Arena**:
   - Use the mouse to choose from one of three backgrounds displayed on the selection screen.
2. **Combat**:
   - Player controls are as follows:
     - **Arrow Keys**: Move left or right.
     - **Up Arrow**: Jump.
     - **1, 2, 3 Keys**: Perform attacks (basic, special, etc.).
     <!-- - **Spacebar**: Block. -->
   - The AI-controlled opponent automatically engages based on the player's position and actions.
3. **Win/Loss Conditions**:
   - The round ends when a fighter's health reaches zero.
   - A victory or defeat message is displayed based on the outcome.
   - The game resets after a brief cooldown period.

---

## Code Structure
The game is implemented using an object-oriented design to ensure modularity and scalability.

### Key Files
1. **`main.py`**:
   - Handles the game loop, background selection, and overall flow.
   - Manages rendering of UI elements like health bars, victory messages, and the arena.

2. **`fighter.py`**:
   - Defines the `Fighter` class, encapsulating attributes and behaviors such as movement, attacks, animations, and health.
   - Includes the `AI` subclass, extending the `Fighter` class with adaptive decision-making for the AI-controlled opponent.

---

### Key Classes and Methods
#### `Fighter` Class
- **Attributes**:
  - Health, velocity, position, and animation states.
- **Methods**:
  - `move`: Manages character movement and actions.
  - `attack`: Handles collision detection and damage application.
  - `update`: Updates animations and state transitions.
  - `draw`: Renders the fighter on the screen.

#### `AI` Subclass
- Extends the `Fighter` class with:
  - Randomized attacks.
  - Strategic movements based on player actions.

---

## Dependencies
- **Python 3**
- **Pygame Library**:
  - Install via pip: `pip install pygame`

---

## Setup and Execution
1. Clone or download the repository to your local machine.
2. Ensure Python 3 and Pygame are installed.
3. Run the game:
   ```bash
   python main.py
   ```
   
---

## Future Enhancements
- Add more fighters with unique abilities.
- Introduce combo systems for advanced gameplay.
- Implement online multiplayer functionality.

---

## Acknowledgments
- Developed by **Oluwasegun Adewola** and **Ifeoluwa Areogun**.
- Special thanks to Professor Sarita Singh for guidance and support.
