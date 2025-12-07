Figure 1 — Mean Human Leading Lag Across Six Dialogues
import matplotlib.pyplot as plt

# Valor medio del lead–lag
mean_lag = 0.47

fig, ax = plt.subplots(figsize=(8, 4))

# Línea vertical en 0 (zero point)
ax.axvline(
    0,
    linestyle="--",
    color="gray",
    alpha=0.7,
    label="Zero point"
)

# Punto medio (X azul)
ax.scatter(
    [mean_lag],
    [0],
    marker="x",
    s=250,
    linewidths=3,
    color="blue",
    label=f"Mean human-leading lag (+{mean_lag:.2f})"
)

# Rango de ejes
ax.set_xlim(-2.0, 2.0)
ax.set_ylim(-1.0, 1.0)
ax.set_yticks([])

# Etiquetas y título
ax.set_xlabel("Lead–Lag (turns)", fontsize=12)
ax.set_title("Mean Human Leading Lag Across Six Dialogues", fontsize=16)

# Grid vertical suave
ax.grid(axis="x", linestyle=":", alpha=0.3)

# Leyenda abajo centrada
ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, -0.25),
    frameon=False,
    ncol=2
)

plt.tight_layout()
plt.savefig("figure_lead_lag.png", dpi=300)
plt.show()


Figure 2 — TIE–Dialog architecture
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np

# ------------------------
# Helpers
# ------------------------
def draw_box(ax, xy, width, height, text, facecolor,
             fontsize=11, bold=False):
    x, y = xy
    box = FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.3, edgecolor="black", facecolor=facecolor
    )
    ax.add_patch(box)
    ax.text(
        x + width / 2,
        y + height / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight="bold" if bold else "normal",
    )
    return box

def arrow(ax, start, end, rad=0.0):
    a = FancyArrowPatch(
        start, end,
        arrowstyle="-|>",
        mutation_scale=10,
        linewidth=1.2,
        color="black",
        connectionstyle=f"arc3,rad={rad}",
    )
    ax.add_patch(a)

# ------------------------
# Figure
# ------------------------
fig, ax = plt.subplots(figsize=(10, 4))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis("off")

# ------------------------
# Dialogue + Turns (izquierda)
# ------------------------
draw_box(ax, (0.6, 5.5), 2.0, 1.0, "Dialogue",
         "#d8e9ff", bold=True)

turn_box = draw_box(ax, (0.7, 2.5), 1.8, 2.4, "",
                    "#e9f1ff")
for y in [4.4, 3.6, 2.8]:
    ax.text(0.7 + 0.9, y, "Turn",
            ha="center", va="center", fontsize=10)

# ------------------------
# Coherence (arriba-centro)
# ------------------------
draw_box(ax, (4.0, 6.2), 3.0, 1.0, "Coherence",
         "#e5ccff", bold=True)

# ------------------------
# Coherence Engine (centro)
# ------------------------
eng = draw_box(ax, (4.0, 2.6), 3.5, 3.2, "",
               "#e0f2df")
ax.text(4.0 + 3.5 / 2, 2.6 + 3.2 - 0.3,
        "Coherence Engine",
        ha="center", va="top",
        fontsize=11, fontweight="bold")

labels = ["Cₜ–Iₘ (matrix)",
          "Cᵢ (per-participant)",
          "Cₜ (global)"]
for i, lab in enumerate(labels):
    y = 3.0 + i * 0.8
    rect = Rectangle(
        (4.2, y), 3.1, 0.6,
        linewidth=1,
        edgecolor="black",
        facecolor="#f7fff7",
    )
    ax.add_patch(rect)
    ax.text(4.2 + 1.55, y + 0.3, lab,
            ha="center", va="center", fontsize=10)

# ------------------------
# Coherence trajectory (derecha)
# ------------------------
plot_x0, plot_y0, plot_w, plot_h = 8.2, 3.0, 3.0, 3.0
ax.add_patch(Rectangle(
    (plot_x0, plot_y0), plot_w, plot_h,
    linewidth=1.3, edgecolor="black", facecolor="white"
))

low = plot_y0 + 0.9
high = plot_y0 + 2.1
ax.hlines([low, high],
          plot_x0 + 0.1,
          plot_x0 + plot_w - 0.1,
          linestyle="dashed", linewidth=1)

# Trayectoria C_t
xs = np.linspace(plot_x0 + 0.1,
                 plot_x0 + plot_w - 0.1, 200)
ys = plot_y0 + 1.5 + 0.7 * np.sin(np.linspace(0, 3 * np.pi, 200))
ax.plot(xs, ys, linewidth=1.7, color="#1f77b4")

# Máximo y mínimo reales de la curva (ahora sí encima)
idx_max = np.argmax(ys)
idx_min = np.argmin(ys)

x_max, y_max = xs[idx_max], ys[idx_max]
x_min, y_min = xs[idx_min], ys[idx_min]

ax.plot(x_min, y_min, "o", color="orange", markersize=8)
ax.plot(x_max, y_max, "o", color="green", markersize=8)

ax.text(plot_x0 + plot_w / 2, plot_y0 + plot_h + 0.2,
        "Dynamic coherence trajectory",
        ha="center", fontsize=9)
ax.text(plot_x0 + plot_w - 0.1, high + 0.25,
        "Stability", ha="right", fontsize=9)
ax.text(plot_x0 + plot_w - 0.1, plot_y0 - 0.2,
        "Matrix", ha="right", va="top", fontsize=9)

# ------------------------
# Rupture module (abajo derecha)
# ------------------------
draw_box(ax, (8.4, 1.3), 2.6, 0.9,
         "Rupture\nDetection",
         "#dddddd", fontsize=9)
draw_box(ax, (8.4, 0.3), 2.6, 0.9,
         "S–B–R\nQuantization",
         "#f0f0f0", fontsize=9)

# ------------------------
# S–B–R global (abajo centro)
# ------------------------
draw_box(ax, (4.6, 0.6), 2.2, 0.9,
         "S–B–R\nQuantization",
         "#e5ccff", fontsize=9)

# ------------------------
# Flechas
# ------------------------
arrow(ax, (2.6, 6.0), (4.0, 6.7))   # Dialogue -> Coherence
arrow(ax, (2.5, 4.0), (4.0, 4.0))   # Turns -> Engine
arrow(ax, (5.5, 6.2), (5.5, 5.8))   # Coherence -> Engine
arrow(ax, (7.5, 4.2), (8.2, 4.5))   # Engine -> trajectory
arrow(ax, (5.75, 2.6), (5.75, 1.5)) # Engine -> S–B–R (centro)
arrow(ax, (9.7, 3.0), (9.7, 2.2))   # trajectory -> Rupture
arrow(ax, (9.7, 1.3), (9.7, 1.2))   # Rupture -> S–B–R (derecha)

plt.tight_layout()
plt.show()

# ------------------------
# SAVE + DOWNLOAD
# ------------------------
plt.savefig("tie_dialog_architecture.png", dpi=300, bbox_inches="tight")

from google.colab import files
files.download("tie_dialog_architecture.png")