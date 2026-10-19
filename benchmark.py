import numpy as np

from routing import make_grid, run_all

SIZE = 100
SEEDS = range(50)
DENSITIES = [0.10, 0.25, 0.35]
ALGOS = ["BFS", "Dijkstra", "A*"]


def benchmark():
    start, goal = (0, 0), (SIZE - 1, SIZE - 1)
    rows = []
    for density in DENSITIES:
        expanded = {a: [] for a in ALGOS}
        costs = []
        no_path = 0
        for seed in SEEDS:
            grid = make_grid(SIZE, SIZE, density=density, seed=seed)
            results = run_all(grid, start, goal)
            if results["BFS"][0] is None:
                # every algorithm must agree that there is no route
                assert all(r[0] is None for r in results.values())
                no_path += 1
                continue
            # every algorithm must agree on the optimal cost
            assert len({r[0] for r in results.values()}) == 1, (density, seed)
            costs.append(results["BFS"][0])
            for a in ALGOS:
                expanded[a].append(results[a][2])
        rows.append((density, len(costs), no_path, np.mean(costs), expanded))
    return rows


def print_table(rows):
    header = f"{'walls':>6} {'solved':>7} {'no path':>8} {'mean cost':>10}"
    for a in ALGOS:
        header += f" {a + ' exp.':>13}"
    header += f" {'A* / Dijkstra':>14}"
    print(header)
    for density, solved, no_path, mean_cost, exp in rows:
        line = f"{density:>6.0%} {solved:>7} {no_path:>8} {mean_cost:>10.1f}"
        means = {a: np.mean(exp[a]) for a in ALGOS}
        for a in ALGOS:
            line += f" {means[a]:>13.0f}"
        line += f" {means['A*'] / means['Dijkstra']:>14.2f}"
        print(line)


if __name__ == "__main__":
    print_table(benchmark())
