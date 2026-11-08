# Algorithmic Game Theory (SPTH WS 26/27)

**Goethe University Frankfurt — Winter Semester 2026/2027**  
*Module: Spieltheorie*

---

## 1. Overview & Motivation

This repository connects **game theory** from the *Spieltheorie* module with **Python implementations** used to explore, test, and verify problem set solutions. Each problem set folder includes:
1. **First-Person Notes & Proofs** in a local `README.md` (covering hand-tested patterns, edge cases caught along the way, game trees, and mathematical arguments).
2. **Backward-Induction Python Solvers** that represent game states as immutable tuples and use caching (`@lru_cache`) to collapse large game trees into compact state graphs.

---

## 2. Core Concepts Used in the Solvers

### Impartial Games
A finite, two-player game of perfect information is **impartial** when the legal moves from a state $s$ depend only on the board/piles, not on whose turn it is.
- **Normal Play:** The last player able to make a move wins.
- **Misère Play:** The player forced to take the last (or poisoned) object loses.

### $\mathcal{P}$-Positions and $\mathcal{N}$-Positions
Using **Zermelo's Theorem** (finite deterministic games without draws have a guaranteed winning strategy for one of the players) and **Backward Induction**, every state falls into one of two buckets:
- **$\mathcal{N}$-Position (Next-Player Winning):** Whoever moves from here can force a win by making at least one move into a $\mathcal{P}$-position.
- **$\mathcal{P}$-Position (Previous-Player Winning / Trap):** Whoever has to move from here loses against optimal play, because *every* legal move hands an $\mathcal{N}$-position to the opponent.

$$
\text{winning}(s) \iff \exists s' \in \text{moves}(s) \text{ such that } \neg\text{winning}(s')
$$

### State Representation & Caching
Raw game trees blow up fast because different move orders often reach the exact same board. By turning every state into a clean **identifier representation** (like sorted tuples `tuple[int, ...]` for Nim piles or `tuple[tuple[int, ...], ...]` for 2D grids) and decorating the evaluator with `@lru_cache(maxsize=None)`, equivalent subtrees merge into a single node with $\mathcal{O}(1)$ lookups.

### Strategic-Form (Normal-Form) Games
In simultaneous-move games (Problem Set 2), players choose strategies at the same time and payoffs are mapped in dictionaries from action-profile tuples $(s_1, \dots, s_n)$ to payoff tuples $(u_1, \dots, u_n)$:
- **Beliefs & Best Responses ($BR_i(\theta_{-i})$):** Weighting payoffs across an opponent's probability distribution $\theta_{-i}$ to find the set of actions that maximize expected utility.
- **Iterated Elimination of Dominated Strategies (IEDS / IEWDS):** Dynamically narrowing active strategy lists by removing actions that are strictly ($>$) or weakly ($\ge$ everywhere, $>$ somewhere) beaten by another pure or mixed strategy across all surviving opponent actions.
- **Pure Nash Equilibrium (PNE):** Action profiles where every player is simultaneously playing a best response to the others (no player can strictly gain by deviating alone).

---

## 3. Repository Structure

```text
algorithmic-game-theory/
├── README.md                           # Main project overview and concept notes
├── requirements.txt                    # Python dependencies (pytest)
├── docs/
│   ├── Problem_Set_1_WS2627.pdf        # Problem Set 1 sheet
│   ├── Problem_Set_2_WS2627.pdf        # Problem Set 2 sheet
│   └── lectures/                       # Lecture notes and supplementary materials
├── core_solvers/                       
│   ├── backward_induction.py           # Reusable backward-induction helper (impartial games)
│   └── normal_form.py                  # Reusable strategic-form game helpers (IEDS, BR, Nash)
├── problem_set_01/
│   ├── README.md                       # Thought process, catches & proofs for PS1
│   ├── misere_nim_solver.py            # Solver for Problem 1 (4-pile Nim)
│   └── chomp_solver.py                 # Solver for Problem 2 (Chomp 2D grid)
└── problem_set_02/
    ├── README.md                       # Thought process, catches & solutions for PS2
    ├── p1_cournot_duopoly.py           # Problem 1: Quantity duopoly & IEDS
    ├── p2_beliefs_best_responses.py    # Problem 2: Expected payoffs & best responses
    ├── p3_dominance_nash.py            # Problem 3: IEDS, IEWDS (mixed) & Pure Nash
    └── p4_student_initiative.py        # Problem 4: 3-player game IEDS & Pure Nash
```

---

## 4. Quick Start

```bash
pip install -r requirements.txt

# Problem Set 01: Impartial Games (Nim & Chomp)
python -m problem_set_01.misere_nim_solver
python -m problem_set_01.chomp_solver

# Problem Set 02: Strategic-Form Games, IEDS/IEWDS & Nash Equilibria
python -m problem_set_02.p1_cournot_duopoly
python -m problem_set_02.p2_beliefs_best_responses
python -m problem_set_02.p3_dominance_nash
python -m problem_set_02.p4_student_initiative
```
