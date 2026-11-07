"""Reusable helpers for finite strategic-form (normal-form) games.

Expected Data Structures:
- 2-Player Matrix: `dict[tuple[str, str], tuple[float, float]]` mapping `(s1, s2) -> (u1, u2)`
- N-Player Matrix: `dict[tuple[str, ...], tuple[float, ...]]` mapping `profile -> payoffs`
- Belief / Mixed Strategy: `dict[str, float]` mapping `action -> probability`
"""

from itertools import product


def find_best_response_2p(matrix, own_actions, belief, player: int):
    """Return `(expected_payoffs, best_responses)` for player 1 or 2 against `belief`."""
    idx = player - 1
    expected_payoffs = {}

    for action in own_actions:
        exp_u = 0.0
        for opp_action, prob in belief.items():
            cell = (action, opp_action) if player == 1 else (opp_action, action)
            exp_u += prob * matrix[cell][idx]
        expected_payoffs[action] = exp_u

    max_u = max(expected_payoffs.values())
    best_responses = [
        act for act, val in expected_payoffs.items() if abs(val - max_u) < 1e-9
    ]
    return expected_payoffs, best_responses


def find_pure_nash_np(matrix, action_spaces):
    """Return all pure Nash equilibrium profiles for an N-player strategic-form game."""
    num_players = len(action_spaces)
    equilibria = []

    for profile in product(*action_spaces):
        is_nash = True
        for i in range(num_players):
            current_u = matrix[profile][i]
            for alt_act in action_spaces[i]:
                if alt_act == profile[i]:
                    continue
                alt_profile = list(profile)
                alt_profile[i] = alt_act
                if matrix[tuple(alt_profile)][i] > current_u:
                    is_nash = False
                    break
            if not is_nash:
                break
        if is_nash:
            equilibria.append(profile)

    return equilibria
