Tic-Tac-Bot
A Reinforcement Learning Approach to Tic-Tac-Toe
Tic-Tac-Bot is a Python implementation of the classic Tic-Tac-Toe game with a focus on AI learning techniques. The project features multiple agent types that play with different strategies, making it an excellent educational resource for studying reinforcement learning in simple game environments.# Tic-Tac-Bot
**A reinforcement-learning take on classic Tic-Tac-Toe**

Tic-Tac-Bot is a small Python project that lets different kinds of agents—reinforcement-learning, minimax, random, or human—battle it out on a 3×3 board. Use it to tinker with reward functions, compare strategies, or just watch AIs trash-talk each other in silence.

---

## Features
- **Plug-and-play agents**  
  - **RL agent** (tabular Q-learning with ε-greedy)  
  - **Minimax solver**  
  - **Pure random**  
  - **Human player**

- **Strategic reward shaping**  
  - Win / loss / draw hierarchy  
  - Positional bonuses (center, corners)  
  - Fork creation & blocking  
  - Two-in-a-row detection  
  - Stage-aware weighting (early vs. late game)

- **Training framework**  
  - Configurable learning rate, discount factor, and exploration schedule  
  - Self-play or vs. fixed opponents

- **Tournament mode**  
  - Round-robin matches  
  - Live ELO updates

---

## Quick Start
```bash
# clone
git clone https://github.com/yourname/tic-tac-bot.git
cd tic-tac-bot

# (optional) create a venv
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# run a quick RL-vs-random training session
python training.py
