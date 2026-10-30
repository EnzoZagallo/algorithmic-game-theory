"""Problem Set 1, Problem 2: Game of Chomp (2D Grid Backward-Induction Solver).

Game Specification:
- Chocolate bar of size m x n represented as an immutable 2D tuple of ints (1 = present, 0 = eaten).
- Consistent with Figure 1 of Problem Set 1, the poisoned piece is located at the
  bottom-right corner: row `m - 1`, col `n - 1`.
- Choosing piece (r, c) removes all pieces (i, j) above and to the left:
  0 <= i <= r and 0 <= j <= c.
- The player forced to eat the poisoned piece (m - 1, n - 1) loses.
"""

from functools import lru_cache

ChompGrid = tuple[tuple[int, ...], ...]


def make_grid(rows: int, cols: int) -> ChompGrid:
    """Create a full m x n Chomp grid of 1s."""
    return tuple(tuple(1 for _ in range(cols)) for _ in range(rows))


@lru_cache(maxsize=None)
def get_transitions(state: ChompGrid) -> list[tuple[str, ChompGrid]]:
    """Generate all valid non-poisoned transitions from `state`.

    Eating piece (r, c) removes all pieces at (i, j) with 0 <= i <= r and 0 <= j <= c.
    """
    transitions: list[tuple[str, ChompGrid]] = []
    rows = len(state)
    cols = len(state[0])

    for r in range(rows):
        for c in range(cols):
            # Skip already-eaten pieces and the bottom-right poisoned piece (rows-1, cols-1)
            if state[r][c] == 1 and not (r == rows - 1 and c == cols - 1):
                new_grid = [list(row) for row in state]
                for i in range(r + 1):
                    for j in range(c + 1):
                        new_grid[i][j] = 0
                next_state = tuple(tuple(row) for row in new_grid)
                action_label = f"Eat piece at row {r}, col {c}"
                transitions.append((action_label, next_state))

    return transitions


@lru_cache(maxsize=None)
def is_winning_state(state: ChompGrid) -> bool:
    """Determine if `state` is an N-position (True) or P-position (False).

    Base case: When only the poisoned piece (bottom-right) remains (`pieces_left == 1`),
    no safe moves exist and the current mover is forced to eat the poison and lose (`False`).
    """
    pieces_left = sum(sum(row) for row in state)
    if pieces_left <= 1:
        return False

    for _, next_state in get_transitions(state):
        if not is_winning_state(next_state):
            return True

    return False


def find_optimal_move(state: ChompGrid) -> tuple[str, ChompGrid] | None:
    """Return the unique or first optimal move `(action_label, next_state)` leading to a P-position."""
    for action, next_state in get_transitions(state):
        if not is_winning_state(next_state):
            return action, next_state
    return None


def main() -> None:
    initial_grid: ChompGrid = make_grid(2, 4)

    print(f"Can P1 force a win on the 2x4 grid? {is_winning_state(initial_grid)}")

    optimal = find_optimal_move(initial_grid)
    if optimal is not None:
        best_action, resulting_state = optimal
        print(f"Player 1's Optimal First Move: {best_action}")
        print("Resulting Grid (P-position trap for Player 2):")
        for row in resulting_state:
            print(f"  {row}")


if __name__ == "__main__":
    main()
