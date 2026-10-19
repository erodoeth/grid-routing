import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from routing import make_grid, manhattan, search

SIZE = 60
start, goal = (0, 0), (SIZE - 1, SIZE - 1)
grid = make_grid(SIZE, SIZE, density=0.30, seed=70)
cost, path, expanded = search(grid, start, goal, manhattan(goal))

fig, ax = plt.subplots(figsize=(6, 6))
ax.imshow(grid, cmap="Greys", vmin=0, vmax=1.4)
ax.plot([c[1] for c in path], [c[0] for c in path], color="tab:red", linewidth=2, label="A* route")
ax.scatter(*start[::-1], color="tab:green", s=60, zorder=3, label="start")
ax.scatter(*goal[::-1], color="tab:blue", s=60, zorder=3, label="goal")
ax.set_title(f"A* on a {SIZE}x{SIZE} grid, 30% walls: cost {cost}, {expanded} nodes expanded")
ax.legend(loc="upper right", fontsize=8)
ax.set_xticks([])
ax.set_yticks([])
fig.tight_layout()
fig.savefig("example.png", dpi=150)
print("saved example.png")
