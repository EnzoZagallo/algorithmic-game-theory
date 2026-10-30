"""Problem Set 1, Problem 1: Four Piles of Matches (2-Bounded Misère Nim Solver).

Game Specification:
- Initial state: Four piles of matches with sizes (1, 1, 2, 2).
- Legal moves: Remove 1 or 2 matches from a single non-empty pile.
- Winning condition (Misère play): The player forced to take the last match loses.
"""

from functools import lru_cache

NimState = tuple[int, ...]


def canonicalize(piles: list[int] | tuple[int, ...]) -> NimState:
    """Return the canonical state: sorted tuple of strictly positive pile sizes."""
    return tuple(sorted(p for p in piles if p > 0))


@lru_cache(maxsize=None)
def get_transitions(state: NimState) -> list[tuple[str, NimState]]:
    """Generate unique canonical transitions from `state` under 2-bounded subtraction."""
    moves: list[tuple[str, NimState]] = []
    seen_states: set[NimState] = set()

    for i, pile_size in enumerate(state):
        for take in range(1, min(2, pile_size) + 1):
            rem = pile_size - take
            new_state = list(state)
            if rem > 0:
                new_state[i] = rem
            else:
                new_state.pop(i)

            canonical_state = tuple(sorted(new_state))
            if canonical_state not in seen_states:
                seen_states.add(canonical_state)
                action = (
                    f"Take {take} from a pile of {pile_size} -> leaves {canonical_state}"
                )
                moves.append((action, canonical_state))

    return moves


@lru_cache(maxsize=None)
def is_winning_state(state: NimState) -> bool:
    """Determine if `state` is an N-position (True) or P-position (False).

    Under Misère convention, if `state == ()`, the previous player just took the
    final match and lost, meaning the current player has already won (`True`).
    Equivalently, `(1,)` forces the current player to take the last match (`False`).
    """
    if len(state) == 0:
        return True

    for _, next_state in get_transitions(state):
        if not is_winning_state(next_state):
            return True
    return False


def get_optimal_move(state: NimState) -> tuple[str, NimState] | None:
    """Return an optimal move `(action, next_state)` that transitions to a P-position."""
    for action, next_state in get_transitions(state):
        if not is_winning_state(next_state):
            return action, next_state
    return None


def enumerate_dag_states(root: NimState = (1, 1, 2, 2)) -> list[NimState]:
    """Return all reachable canonical states from `root` ordered by total matches."""
    visited: set[NimState] = set()
    stack = [root]
    while stack:
        curr = stack.pop()
        if curr not in visited:
            visited.add(curr)
            for _, nxt in get_transitions(curr):
                stack.append(nxt)
    return sorted(visited, key=lambda s: (sum(s), len(s), s), reverse=True)


def main() -> None:
    initial_state: NimState = (1, 1, 2, 2)
    p1_can_win = is_winning_state(initial_state)

    print(f"Is {initial_state} a winning position for P1? {p1_can_win}")
    print("Result: (1, 1, 2, 2) is a P-position. Player 2 has a guaranteed winning strategy.\n")

    print("--- Player 2's Optimal Winning Responses to Every P1 Opening Move ---")
    for action_p1, state_after_p1 in get_transitions(initial_state):
        optimal_p2 = get_optimal_move(state_after_p1)
        if optimal_p2 is not None:
            best_action_p2, state_after_p2 = optimal_p2
            print(f"If P1 plays:   {action_p1}")
            print(f"   P2 responds: {best_action_p2}")
            print(
                f"   State left:  {state_after_p2} "
                f"(P-position trap: {not is_winning_state(state_after_p2)})\n"
            )

    print("--- Complete DAG Partition (P-positions vs. N-positions) ---")
    for state in enumerate_dag_states(initial_state):
        classification = "N-position (Winning)" if is_winning_state(state) else "P-position (Losing Trap)"
        print(f"State {str(state):<14} | Total Matches: {sum(state)} | {classification}")


if __name__ == "__main__":
    main()
