"""Problem Set 2, Problem 1: Two Firms Compete in Quantities (Discrete Cournot Duopoly)."""
ACTIONS = (1, 3, 5)  # Small, Medium, Large
C1, C2 = 2, 3

def compute_payoffs(q1: int, q2: int) -> tuple[int, int]:
    price = 10 - q1 - q2
    pi_1 = (price - C1) * q1
    pi_2 = (price - C2) * q2
    return (pi_1, pi_2)

def build_strategic_form(actions_1: tuple[int, ...], actions_2: tuple[int, ...]) -> dict[tuple[int, int], tuple[int, int]]:
    """Stores all combinations and maps (q1, q2) -> (pi_1, pi_2)."""
    matrix = {}
    for q1 in actions_1:
        for q2 in actions_2:
            matrix[(q1, q2)] = compute_payoffs(q1, q2)
    return matrix

def run_ieds(
    matrix: dict[tuple[int, int], tuple[int, int]],
    actions_1: tuple[int, ...], 
    actions_2: tuple[int, ...]
) -> tuple[list[int], list[int]]: 
    """Iteratively eliminates strictly dominated pure strategies and returns surviving strategies."""
    active_q1 = list(actions_1)
    active_q2 = list(actions_2)
    round_num = 1

    while True:
        changed = False
        print(f"--- IEDS Round {round_num} ---")
        # Checking firm 1 for strictly dominated strategies (row player)
        to_remove_q1 = []
        for s1 in active_q1:
            for alt_s1 in active_q1:
                if s1 == alt_s1:
                    continue
                if all(matrix[(alt_s1, q2)][0] > matrix[(s1, q2)][0] for q2 in active_q2):
                    print(f"Firm 1: q1={s1} is strictly dominated by q1={alt_s1}")
                    to_remove_q1.append(s1)
                    break
        for s1 in to_remove_q1:
            active_q1.remove(s1)
            changed = True
        # Checking firm 2 for strictly dominated strategies (column player) against firm 1's updated surviving strategies #
        to_remove_q2 = []
        for s2 in active_q2:
            for alt_s2 in active_q2:
                if s2 == alt_s2:
                    continue
                # Does alt_s2 strictly dominate s2 across ALL surviving active_q1?
                if all(matrix[(q1, alt_s2)][1] > matrix[(q1, s2)][1] for q1 in active_q1):
                    print(f"Firm 2: q2={s2} is strictly dominated by q2={alt_s2}")
                    to_remove_q2.append(s2)
                    break
        for s2 in to_remove_q2:
            active_q2.remove(s2)
            changed = True

        if not changed:
            print("No further eliminations possible. Convergence reached!\n")
            break
            
        round_num += 1
    return active_q1, active_q2

class Node:
    def __init__(
        self,
        player: str | None = None,
        info_set: str | None = None,
        payoffs: tuple[int, int] | None = None
    ):
        self.player = player          # "Firm 1", "Firm 2", or None (Terminal)
        self.info_set = info_set      # Shared ID represents simultaneous moves
        self.payoffs = payoffs        # (pi_1, pi_2) at terminal leaves
        self.children: dict[int, Node] = {}  # Maps action -> child Node

    def is_terminal(self) -> bool:
        return self.payoffs is not None


def build_extensive_form(actions_1: tuple[int, ...], actions_2: tuple[int, ...]) -> Node:
    """Builds the extensive-form game tree with shared information set I2."""
    root = Node(player="Firm 1", info_set="I1")
    
    for q1 in actions_1:
        # All of Firm 2's decision nodes share info_set="I2" (dashed line)
        f2_node = Node(player="Firm 2", info_set="I2")
        root.children[q1] = f2_node
        
        for q2 in actions_2:
            leaf_payoffs = compute_payoffs(q1, q2)
            f2_node.children[q2] = Node(payoffs=leaf_payoffs)
            
    return root

if __name__ == "__main__":
    matrix = build_strategic_form(ACTIONS, ACTIONS)
    
    print("Strategic Form Payoff Matrix:")
    for q1 in ACTIONS:
        row_str = " | ".join(f"{str(matrix[(q1, q2)]):>9}" for q2 in ACTIONS)
        print(f"q1={q1}: {row_str}")
    print()

    surviving_q1, surviving_q2 = run_ieds(matrix, ACTIONS, ACTIONS)
    print(f"Surviving Strategies: Firm 1 -> {surviving_q1}, Firm 2 -> {surviving_q2}")
    
    tree_root = build_extensive_form(ACTIONS, ACTIONS)
    print(f"Root Player: {tree_root.player} | Branches: {list(tree_root.children.keys())}")
    print(f"Firm 2 Info Sets across branches: {[child.info_set for child in tree_root.children.values()]}")