# Tic-Tac-Bot  
**A reinforcement-learning take on classic Tic-Tac-Toe**

Tic-Tac-Bot is a Python implementation of Tic-Tac-Toe with multiple agent types—RL, minimax, random, or human.
---

## Features

- **Easy-to-plug agents**  
  - **RL agent** (tabular Q-learning with ε-greedy)  
  - **Minimax**  
  - **random**  
  - **Human**

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
