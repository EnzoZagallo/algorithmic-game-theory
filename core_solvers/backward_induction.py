"""Reusable backward-induction solver for finite impartial games.

Expected Data Structures:
- `state`: Any immutable, hashable object (e.g., `tuple[int, ...]` for piles
  or `tuple[tuple[int, ...], ...]` for 2D grids) so `@lru_cache` can index it.
- `get_transitions(state)`: Function returning `list[tuple[str, state]]`, where
  each item is `(move_description, next_state)`.
- `terminal_value(state)`: Function returning `True` or `False` if `state` is a
  base/terminal case, or `None` if moves still need to be evaluated.

Mechanism:
- Memoizes every visited state with `@lru_cache(maxsize=None)` for O(1) lookups.
- Tracks turns implicitly: a state is winning (`True`) if at least one move leaves
  the next player in a losing state (`not is_winning_state(next_state)`).
"""

from functools import lru_cache


def build_solver(get_transitions, terminal_value):
    """Return `(is_winning_state, get_optimal_move)` for a given game."""

    @lru_cache(maxsize=None)
    def is_winning_state(state) -> bool:
        base = terminal_value(state)
        if base is not None:
            return base

        for _, next_state in get_transitions(state):
            if not is_winning_state(next_state):
                return True
        return False

    def get_optimal_move(state):
        for action, next_state in get_transitions(state):
            if not is_winning_state(next_state):
                return action, next_state
        return None

    return is_winning_state, get_optimal_move
