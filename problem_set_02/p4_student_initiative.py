"""Problem Set 2, Problem 4: Joining a Student Initiative (3-Player Static Game)."""

from itertools import product

ACTIONS = ("J", "H")  # Join or Stay Home


def compute_payoffs(
    profile: tuple[str, str, str],
    b: tuple[int, int, int],
) -> tuple[int, int, int]:
    """Compute (u1, u2, u3) for a 3-student action profile (s1, s2, s3).

    u_i(H) = 0
    u_i(J) = b_i + 2*k_i - 4, where k_i is the number of other students joining.
    """
    payoffs = []
    for i in range(3):
        if profile[i] == "H":
            payoffs.append(0)
        else:
            k_i = sum(1 for j in range(3) if j != i and profile[j] == "J")
            u_i = b[i] + 2 * k_i - 4
            payoffs.append(u_i)
    return (payoffs[0], payoffs[1], payoffs[2])


def build_game_matrix(
    b: tuple[int, int, int],
) -> dict[tuple[str, str, str], tuple[int, int, int]]:
    """Store all 2x2x2 = 8 combinations mapping (s1, s2, s3) -> (u1, u2, u3)."""
    matrix = {}
    for profile in product(ACTIONS, repeat=3):
        matrix[profile] = compute_payoffs(profile, b)
    return matrix


def run_ieds_3p(
    matrix: dict[tuple[str, str, str], tuple[int, int, int]],
) -> list[list[str]]:
    """Iteratively eliminate strictly dominated strategies for all 3 students."""
    active = [list(ACTIONS) for _ in range(3)]
    round_num = 1

    while True:
        changed = False
        print(f"--- IEDS Round {round_num} ---")
        round_removals: list[tuple[int, str]] = []

        for i in range(3):
            if len(active[i]) <= 1:
                continue

            other_indices = [j for j in range(3) if j != i]
            opp_combinations = list(
                product(active[other_indices[0]], active[other_indices[1]])
            )

            for s_i in active[i]:
                for alt_i in active[i]:
                    if s_i == alt_i:
                        continue

                    # Check if alt_i > s_i across all surviving opponent combinations
                    strictly_better_all = True
                    for opp_0, opp_1 in opp_combinations:
                        prof_alt = ["", "", ""]
                        prof_cur = ["", "", ""]
                        prof_alt[i], prof_cur[i] = alt_i, s_i
                        prof_alt[other_indices[0]] = prof_cur[other_indices[0]] = opp_0
                        prof_alt[other_indices[1]] = prof_cur[other_indices[1]] = opp_1

                        if matrix[tuple(prof_alt)][i] <= matrix[tuple(prof_cur)][i]:
                            strictly_better_all = False
                            break

                    if strictly_better_all:
                        print(
                            f"Student {i + 1}: '{s_i}' is strictly dominated by '{alt_i}'"
                        )
                        round_removals.append((i, s_i))
                        break

        for i, s_i in round_removals:
            active[i].remove(s_i)
            changed = True

        if not changed:
            print(
                f"Convergence reached! Surviving: "
                f"S1={active[0]}, S2={active[1]}, S3={active[2]}\n"
            )
            break

        round_num += 1

    return active


def find_pure_nash_3p(
    matrix: dict[tuple[str, str, str], tuple[int, int, int]],
) -> list[tuple[str, str, str]]:
    """Find all pure Nash equilibria (s1, s2, s3) where no student wants to deviate."""
    nash_equilibria = []

    for profile in product(ACTIONS, repeat=3):
        is_nash = True
        for i in range(3):
            current_payoff = matrix[profile][i]
            alt_action = "H" if profile[i] == "J" else "J"
            alt_profile = list(profile)
            alt_profile[i] = alt_action
            alt_payoff = matrix[tuple(alt_profile)][i]

            if alt_payoff > current_payoff:
                is_nash = False
                break
        if is_nash:
            nash_equilibria.append(profile)

    return nash_equilibria


if __name__ == "__main__":
    # Part 1: Run IEDS
    b_part1 = (5, 3, 1)
    matrix_part1 = build_game_matrix(b_part1)
    print(f"=== Part 1: IEDS with b = {b_part1} ===")
    surviving_part1 = run_ieds_3p(matrix_part1)

    # Part 2: Find all Pure Nash Equilibria
    b_part2 = (3, 3, 1)
    matrix_part2 = build_game_matrix(b_part2)
    print(f"=== Part 2: Pure Nash Equilibria with b = {b_part2} ===")
    ne_part2 = find_pure_nash_3p(matrix_part2)
    for prof in ne_part2:
        print(f"Profile {prof} with payoffs {matrix_part2[prof]}")
