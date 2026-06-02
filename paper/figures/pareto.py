"""Generate paper/figures/pareto.pdf for Cross-Axis Correction.

Axes:
    x = benign preservation (AlpacaEval, %)
    y = strict refusal (WildJailbreak, %)

Encoding:
    Shape  — circle = Qwen3-32B, square = Llama-3.3-70B-Instruct
    Fill   — filled = cross-axis, open = single-axis
    Colour — blue = Qwen3-32B, orange = Llama-3.3-70B-Instruct
    Arrow  — single-axis -> cross-axis per model
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import matplotlib.lines as mlines

# (benign_preserved, strict_refusal)
qwen_single  = (90.0, 32.9)
qwen_cross   = (91.0, 54.5)
llama_single = (99.0, 20.6)
llama_cross  = (98.0, 48.1)

BLUE   = "#1f77b4"
ORANGE = "#ff7f0e"
S      = 80      # marker size
LW     = 0.8     # marker edge linewidth

fig, ax = plt.subplots(figsize=(3.4, 2.8))

# --- Qwen3-32B (circles) ---
ax.scatter(*qwen_single, s=S, marker="o", facecolor="white",
           edgecolor=BLUE, linewidth=LW, zorder=3)
ax.scatter(*qwen_cross,  s=S, marker="o", facecolor=BLUE,
           edgecolor=BLUE, linewidth=LW, zorder=3)

# --- Llama-3.3-70B-Instruct (squares) ---
ax.scatter(*llama_single, s=S, marker="s", facecolor="white",
           edgecolor=ORANGE, linewidth=LW, zorder=3)
ax.scatter(*llama_cross,  s=S, marker="s", facecolor=ORANGE,
           edgecolor=ORANGE, linewidth=LW, zorder=3)

# --- Arrows: single -> cross ---
for (sx, sy), (cx, cy), color in [
    (qwen_single,  qwen_cross,  BLUE),
    (llama_single, llama_cross, ORANGE),
]:
    ax.add_patch(FancyArrowPatch(
        (sx, sy), (cx, cy),
        arrowstyle="-|>", mutation_scale=10,
        color=color, linewidth=1.1, zorder=2,
    ))

# --- Model annotations along arrows ---
ax.annotate("Qwen3-32B", xy=(90.5, 43.5), fontsize=7,
            color=BLUE, ha="left", va="center")
ax.annotate("Llama-3.3-70B", xy=(97.2, 33.5), fontsize=7,
            color=ORANGE, ha="right", va="center")

# --- Legend: filled = cross-axis, open = single-axis ---
legend_handles = [
    mlines.Line2D([], [], marker="o", linestyle="None",
                  markersize=6, markerfacecolor="#555555",
                  markeredgecolor="#555555", label="Cross-axis"),
    mlines.Line2D([], [], marker="o", linestyle="None",
                  markersize=6, markerfacecolor="white",
                  markeredgecolor="#555555", label="Single-axis"),
]
ax.legend(handles=legend_handles, fontsize=7, loc="lower left",
          framealpha=0.9, borderpad=0.6)

# --- Axes ---
ax.set_xlabel("Benign preservation on AlpacaEval (%)", fontsize=8)
ax.set_ylabel("Strict refusal on WildJailbreak (%)", fontsize=8)
ax.set_xlim(84, 102)
ax.set_ylim(12, 65)
ax.tick_params(labelsize=7)
ax.grid(True, linestyle=":", linewidth=0.5, alpha=0.6)
ax.set_axisbelow(True)

fig.tight_layout()
fig.savefig("pareto.pdf", bbox_inches="tight")
print("Wrote pareto.pdf")
