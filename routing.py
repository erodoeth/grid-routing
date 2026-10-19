import heapq
from collections import deque

import numpy as np


def make_grid(rows, cols, density=0.25, seed=70):
    rng = np.random.default_rng(seed)
    grid = (rng.random((rows, cols)) < density).astype(int)
    grid[0, 0] = grid[-1, -1] = 0  # keep start and goal open
    return grid


def neighbours(grid, cell):
    rows, cols = grid.shape
    row, col = cell
    result = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols and grid[new_row, new_col] == 0:
            result.append((new_row, new_col))
    return result


def manhattan(goal):
    return lambda c: abs(c[0] - goal[0]) + abs(c[1] - goal[1])


def _rebuild_path(parent, cell):
    path = []
    while cell is not None:
        path.append(cell)
        cell = parent[cell]
    return path[::-1]


def bfs(grid, start, goal):
    queue = deque([start])
    dist = {start: 0}
    parent = {start: None}
    expanded = 0

    while queue:
        cell = queue.popleft()
        expanded += 1
        if cell == goal:
            return dist[cell], _rebuild_path(parent, cell), expanded
        for nb in neighbours(grid, cell):
            if nb not in dist:
                dist[nb] = dist[cell] + 1
                parent[nb] = cell
                queue.append(nb)
    return None, None, expanded


def search(grid, start, goal, heuristic=None):
    h = heuristic or (lambda c: 0)
    heap = [(h(start), 0, start)]
    best = {start: 0}
    parent = {start: None}
    expanded = 0

    while heap:
        _, neg_g, cell = heapq.heappop(heap)
        cost = -neg_g
        if cost > best[cell]:  
            continue
        expanded += 1
        if cell == goal:
            return cost, _rebuild_path(parent, cell), expanded
        for nb in neighbours(grid, cell):
            new_cost = cost + 1
            if new_cost < best.get(nb, float("inf")):
                best[nb] = new_cost
                parent[nb] = cell
                heapq.heappush(heap, (new_cost + h(nb), -new_cost, nb))
    return None, None, expanded


def run_all(grid, start, goal):
       return {
        "BFS": bfs(grid, start, goal),
        "Dijkstra": search(grid, start, goal),
        "A*": search(grid, start, goal, manhattan(goal)),
    }


if __name__ == "__main__":
    grid = make_grid(100, 100)
    results = run_all(grid, (0, 0), (99, 99))
    print("Random grid (100x100, 25% walls)")
    for name, (cost, _, expanded) in results.items():
        print(f"  {name:9s} cost {cost}  expanded {expanded}")
    assert len({r[0] for r in results.values()}) == 1

    grid = np.zeros((20, 20), dtype=int)
    grid[10, :] = 1
    grid[10, 19] = 0
    results = run_all(grid, (0, 0), (19, 0))
    print("Wall grid (20x20)")
    for name, (cost, _, expanded) in results.items():
        print(f"  {name:9s} cost {cost}  expanded {expanded}")
    assert all(r[0] == 57 for r in results.values())

    grid = np.zeros((5, 5), dtype=int)
    grid[3, :] = 1
    assert search(grid, (0, 0), (4, 4))[0] is None
    assert bfs(grid, (0, 0), (4, 4))[0] is None
    print("No-path case handled")
