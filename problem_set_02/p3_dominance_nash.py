"""Problem Set 2, Problem 3: Dominated Strategies (IEDS / IEWDS) & Pure Nash Equilibria."""
from itertools import combinations

ROWS = ("A", "B", "C", "D")
COLS = ("a", "b", "c", "d")

# 4x4 Payoff matrix mapping (row, col) -> (u1,u2)
MATRIX: dict[tuple[str, str], tuple[int, int]] = {
    ("A", "a"): (4, 4), ("A", "b"): (0, 0), ("A", "c"): (5, 1), ("A", "d"): (0, 0),
    ("B", "a"): (0, 0), ("B", "b"): (4, 4), ("B", "c"): (5, 1), ("B", "d"): (0, 0),
    ("C", "a"): (0, 0), ("C", "b"): (0, 0), ("C", "c"): (2, 1), ("C", "d"): (0, 0),
    ("D", "a"): (1, 0), ("D", "b"): (1, 0), ("D", "c"): (5, 3), ("D", "d"): (0, 0),  
}

def generate_candidates(active_actions: list[str]) -> list[tuple[str, dict[str, float]]]:
    """
    Generating all pure strategies and pairwise mixed strategies.

    """
    candidates = []

    # 1. Pure strategies 
    for act in active_actions:
        candidates.append((f"Pure {act}", {act: 1.0}))
    # 2. Mixed strategies
    for act1, act2 in combinations(active_actions,2):
        label = f"Mix(0.5*{act1} + 0.5*{act2})"
        candidates.append((label, {act1: 0.5, act2: 0.5}))

    return candidates

def expected_payoff_vs_pure(
    matrix: dict[tuple[str, str], tuple[int, int]],
    sigma: dict[str, float],
    opp_action: str,
    player: int      
) -> float:
    idx = player - 1
    total = 0.0
    for own_act, prob in sigma.items():
        cell = (own_act, opp_action) if player == 1 else (opp_action, own_act)
        total += prob * matrix[cell][idx]
    return total

def is_dominated(
    matrix: dict[tuple[str, str], tuple[int, int]],
    target_act: str,
    alt_sigma: dict[str, float],
    opp_active: list[str],
    player: int,
    weak: bool = False
) -> bool:
    """Check if a pure strategy is strictly or weakly dominated by `alt_sigma`."""

    target_sigma = {target_act: 1.0}

    comparisons_ge = []
    comparisons_gt = []

    for opp_act in opp_active:
        u_alt = expected_payoff_vs_pure(matrix, alt_sigma, opp_act, player)
        u_target = expected_payoff_vs_pure(matrix, target_sigma, opp_act, player)

        comparisons_ge.append(u_alt >= u_target - 1e-9)
        comparisons_gt.append(u_alt > u_target + 1e-9)

    if not weak:
        return all(comparisons_gt)
    else:
        return all(comparisons_ge) and any(comparisons_gt)

def run_elimination(
    matrix: dict[tuple[str, str], tuple[int, int]],
    rows: tuple[str, ...],
    cols: tuple[str, ...],
    weak: bool = False
) -> tuple[list[str], list[str]]:
    """Iteratively remove strictly or weakly dominated strategies."""
    active_rows = list(rows)
    active_cols = list(cols)
    mode = "IEWDS (Weak)" if weak else "IEDS (Strict)"
    round_num = 1
    print(f"Running {mode}")
    while True:
        changed = False
        # Player 1
        to_remove_rows = []
        row_candidates = generate_candidates(active_rows)
        for r in active_rows:
            for label, sigma in row_candidates:
                if sigma == {r: 1.0}:
                    continue
                if is_dominated(matrix, r, sigma, active_cols, player=1, weak=weak):
                    print(f"Round {round_num} (P1): Row '{r}' eliminated by {label}")
                    to_remove_rows.append(r)
                    break
        for r in to_remove_rows:
            active_rows.remove(r)
            changed = True
        # Player 2
        to_remove_cols = []
        col_candidates = generate_candidates(active_cols)
        for c in active_cols:
            for label, sigma in col_candidates:
                if sigma == {c: 1.0}:
                    continue
                if is_dominated(matrix, c, sigma, active_rows, player=2, weak=weak):
                    print(f"Round {round_num} (P2): Col '{c}' eliminated by {label}")
                    to_remove_cols.append(c)
                    break
        for c in to_remove_cols:
            active_cols.remove(c)
            changed = True

        if not changed:
            print(f"No more rows and columns to eliminate, the surviving rows and columns are:P1={active_rows}, P2={active_cols}\n")
            break
        
        round_num += 1

    return active_rows, active_cols
    
    


def find_pure_nash_equilibria(
    matrix: dict[tuple[str, str], tuple[int, int]],
    rows: tuple[str, ...],
    cols: tuple[str, ...]
) -> list[tuple[str, str]]:
     nash_equilibria = []
     for r in rows:
        for c in cols:
            u1, u2 = matrix[(r, c)]
            max_u1_in_col = max(matrix[(alt_r, c)][0] for alt_r in rows)
            max_u2_in_row = max(matrix[(r, alt_c)][1] for alt_c in cols)
            if u1 == max_u1_in_col and u2 == max_u2_in_row:
                 nash_equilibria.append((r, c))
     return nash_equilibria

if __name__ == "__main__":
    # IEDS (Strict Dominance)
    ieds_rows, ieds_cols = run_elimination(MATRIX, ROWS, COLS, weak=False)

    # IEWDS (Weak Dominance)
    iewds_rows, iewds_cols = run_elimination(MATRIX, ROWS, COLS, weak=True)

    # Pure Nash Equilibria
    pure_ne = find_pure_nash_equilibria(MATRIX, ROWS, COLS)
    print("=== Part 3: Pure Nash Equilibria ===")
    for r, c in pure_ne:
        print(f"Profile ({r}, {c}) with payoffs {MATRIX[(r, c)]}")