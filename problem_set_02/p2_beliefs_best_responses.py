"""Problem Set 2, Problem 2: Beliefs and Best Responses."""

ROWS = ("U", "M", "D")
COLS = ("L", "C", "R")

#Payoff matrix mapping (s1, s2) -> (u1, u2)
MATRIX: dict[tuple[str, str], tuple[int, int]] = {
    ("U", "L"): (3, 2), ("U", "C"): (0, 4), ("U", "R"): (6, 1),
    ("M", "L"): (2, 5), ("M", "C"): (5, 1), ("M", "R"): (1, 3),
    ("D", "L"): (4, 0), ("D", "C"): (2, 3), ("D", "R"): (3, 6),
}

def get_pure_payoff(
    matrix: dict[tuple[str, str], tuple[int, int]],
    s1: str,
    s2: str,
    player: int,
) -> int:
    """Return u_i(s1, s2) for player 1 or 2 using 0-based tuple indexing."""
    return matrix[(s1, s2)][player - 1]

def find_best_response(
    matrix: dict[tuple[str, str], tuple[int, int]],
    own_actions: tuple[str, ...],
    belief: dict[str, float],
    player: int
) -> tuple[dict[str, float], list[str]]:
    expected_payoffs: dict[str, float] = {}
    idx = player - 1

    for action in own_actions:
        exp_u = 0.0
        for opp_action, prob in belief.items():
            cell = (action, opp_action) if player == 1 else (opp_action, action)
            exp_u += prob * matrix[cell][idx]
        expected_payoffs[action] = exp_u 

    max_u = max(expected_payoffs.values())
    best_responses = [act for act, val in expected_payoffs.items() if abs(val - max_u) < 1e-9]

    return expected_payoffs, best_responses

def compute_mixed_payoff(
    matrix: dict[tuple[str, str], tuple[int, int]],
    sigma_1: dict[str, float],
    sigma_2: dict[str, float],
    player: int      
) -> float:
    total_expected_u = 0.0
    for s1, prob_1 in sigma_1.items():
        for s2, prob_2 in sigma_2.items():
            join_weight = prob_1 * prob_2
            payoff = get_pure_payoff(matrix, s1, s2, player)
            total_expected_u += join_weight * payoff
    return total_expected_u

# All 3 core functions are defined above, and the payoff matrix data is stored cleanly.

if __name__ == "__main__":
    # Part 1: Pure Strategy Lookups
    print("Pure Payoffs")
    print(f"u1(U, R) = {get_pure_payoff(MATRIX, 'U', 'R', player=1)}")
    print(f"u2(M, L) = {get_pure_payoff(MATRIX, 'M', 'L', player=2)}")
    print(f"u1(D, C) = {get_pure_payoff(MATRIX, 'D', 'C', player=1)}\n")

    #Part 2: Player 1's expected payoffs and BR1(theta_2)
    theta_2 = {"L": 0.5, "C": 0.25, "R": 0.25}
    exp_u1, br_1 = find_best_response(MATRIX, ROWS, theta_2, player=1)
    print("Part 2: Player 1 Best Response")
    print(f"Expected Payoffs for P1: {exp_u1}")
    print(f"BR1(theta_2) = {br_1}\n")

    #Part 3: Player 2's expected payoffs and BR2(theta_1)
    theta_1 = {"U": 0.5, "M": 0.0, "D": 0.5}
    exp_u2, br_2 = find_best_response(MATRIX, COLS, theta_1, player=2)
    print("Part 3: Player 2 Best Response")
    print(f"Expected Payoffs for P2: {exp_u2}")
    print(f"BR2(theta_1) = {br_2}\n")

    #Part 4: Expected Payoff u2(sigma_1, sigma_2)
    sigma_1 = {"U": 0.5, "M": 0.0, "D": 0.5}
    sigma_2 = {"L": 0.0, "C": 0.5, "R": 0.5}
    u2_mixed = compute_mixed_payoff(MATRIX, sigma_1, sigma_2, player=2)
    print("Part 4: Mixed Strategy Payoff")
    print(f"u2(sigma_1, sigma_2) = {u2_mixed}")