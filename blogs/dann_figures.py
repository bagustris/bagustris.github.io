"""Figures for the post "Domain Adversarial Neural Network (DANN), Explained Simply".

The toy training in Fig. 3 is a hand-written numpy DANN (linear feature extractor,
logistic task head, logistic domain head behind a gradient-reversal step).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = "images/dann"
BLUE, RED, GRAY, GREEN, ORANGE = "#2b6cb0", "#c53030", "#718096", "#2f855a", "#dd6b20"
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})


# ---- Fig 1: architecture --------------------------------------------
def box(ax, xy, w, h, text, color, fc=None):
    ax.add_patch(FancyBboxPatch(xy, w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                ec=color, fc=fc or "white", lw=2))
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha="center", va="center", color=color, fontweight="bold")


def arrow(ax, a, b, color="k", **kw):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=16, color=color, lw=2, **kw))


fig, ax = plt.subplots(figsize=(11, 4.6))
ax.set(xlim=(0, 11), ylim=(0, 4.6)); ax.axis("off")
box(ax, (0.2, 1.8), 1.5, 1.0, "input\naudio x", GRAY)
box(ax, (2.5, 1.8), 2.0, 1.0, "shared model\n(feature extractor)", BLUE)
box(ax, (5.6, 3.1), 2.0, 1.0, "task head\nreal / fake", GREEN)
box(ax, (5.6, 0.5), 1.0, 1.0, "GRL", RED, "#fed7d7")
box(ax, (7.2, 0.5), 2.2, 1.0, "domain head\nwhich database?", ORANGE)
box(ax, (9.9, 3.1), 1.0, 1.0, "L_task", GREEN)
box(ax, (9.9, 0.5), 1.0, 1.0, "L_dom", ORANGE)
arrow(ax, (1.7, 2.3), (2.5, 2.3))
arrow(ax, (4.5, 2.5), (5.6, 3.5)); arrow(ax, (4.5, 2.1), (5.6, 1.1))
ax.text(5.05, 2.35, "features h", ha="center", color=BLUE, fontsize=10)
arrow(ax, (6.6, 1.0), (7.2, 1.0)); arrow(ax, (7.6, 3.6), (9.9, 3.6)); arrow(ax, (9.4, 1.0), (9.9, 1.0))
ax.text(6.6, 2.75, "backward: \"make h better for real/fake\"", color=GREEN, fontsize=10, ha="center")
ax.text(6.6, 0.05, "backward: gradient is FLIPPED by the GRL \u2192 \"make h worse for guessing the database\"",
        color=RED, fontsize=10, ha="center")
fig.savefig(f"{OUT}/01-architecture.png", dpi=150, bbox_inches="tight")

# ---- Fig 2: gradient reversal ----------------------------------------
fig, axs = plt.subplots(1, 2, figsize=(10, 2.6))
for ax, ttl, lab, col in [(axs[0], "Forward pass", r"$\mathrm{GRL}(h)=h$  (identity)", BLUE),
                          (axs[1], "Backward pass", r"$\dfrac{\partial\,\mathrm{GRL}}{\partial h}=-\lambda$  (flip & scale)", RED)]:
    ax.axis("off"); ax.set_title(ttl, color=col, fontweight="bold")
    box(ax, (0.05, 0.3), 0.25, 0.4, "model", BLUE); box(ax, (0.4, 0.3), 0.2, 0.4, "GRL", RED, "#fed7d7")
    box(ax, (0.7, 0.3), 0.25, 0.4, "domain\nhead", ORANGE)
    ax.set(xlim=(0, 1), ylim=(0, 1))
    if col == BLUE:
        arrow(ax, (0.30, 0.5), (0.4, 0.5), BLUE); arrow(ax, (0.6, 0.5), (0.7, 0.5), BLUE)
    else:
        arrow(ax, (0.7, 0.2), (0.6, 0.2), RED); arrow(ax, (0.4, 0.2), (0.30, 0.2), RED)
        ax.text(0.5, 0.08, r"$g \;\rightarrow\; -\lambda g$", ha="center", color=RED)
    ax.text(0.5, 0.85, lab, ha="center", fontsize=13)
fig.savefig(f"{OUT}/02-grl.png", dpi=150, bbox_inches="tight")

# ---- Fig 3: toy numpy DANN -------------------------------------------
# Shortcut setup: in the TRAINING data, database B is mostly fake and database A mostly real.
# In the unseen TEST database the link is reversed, so a model that learned "database = label" fails.
u = np.array([1.0, 0.3]); u /= np.linalg.norm(u)      # direction that really separates real/fake
v = np.array([-0.3, 1.0]); v /= np.linalg.norm(v)     # direction that separates database A/B
sig = lambda a: 1 / (1 + np.exp(-a))


def make(seed, n, p_fake_B):
    r = np.random.default_rng(seed)
    dom = np.repeat([0, 1], n)
    cls = (r.random(2 * n) < np.where(dom == 1, p_fake_B, 1 - p_fake_B)).astype(int)
    X = r.normal(0, 0.6, (2 * n, 2)) + np.outer(cls * 2 - 1, u) * 0.9 + np.outer(dom * 2 - 1, v) * 1.5
    return X, cls, dom


X, cls, dom = make(0, 300, 0.85)
Xt, ct, dt = make(5, 300, 0.15)


def train(lam, epochs=3000, lr=0.3):
    w = np.array([0.1, 0.1]); wt = wd = 1.0; bt = bd = 0.0; hist = []
    for _ in range(epochs):
        h = X @ w
        pt, pd_ = sig(h * wt + bt), sig(h * wd + bd)
        et, ed = (pt - cls) / len(X), (pd_ - dom) / len(X)       # dLoss/dlogit
        gh = et * wt - lam * ed * wd                            # gradient reaching the feature: task - lambda * domain
        w = w - lr * (X.T @ gh)
        wt -= lr * np.sum(h * et); bt -= lr * et.sum()
        wd -= lr * np.sum(h * ed); bd -= lr * ed.sum()
        hist.append((((pt > .5) == cls).mean(), ((pd_ > .5) == dom).mean()))
    test = ((sig(Xt @ w * wt + bt) > .5) == ct).mean()
    return w, np.array(hist), test


w0, h0, t0 = train(0.0)
w1, h1, t1 = train(2.0)

fig, axs = plt.subplots(1, 3, figsize=(14, 4))
ax = axs[0]
for d, mk in [(0, "o"), (1, "s")]:
    for c, col in [(0, GREEN), (1, RED)]:
        m = (dom == d) & (cls == c)
        ax.scatter(X[m, 0], X[m, 1], s=12, marker=mk, c=col, alpha=.45)
for w, col, lab in [(w0, GRAY, "no DANN"), (w1, BLUE, "with DANN")]:
    d = w / np.linalg.norm(w) * 2.6
    ax.annotate("", d, (0, 0), arrowprops=dict(arrowstyle="-|>", color=col, lw=3))
    ax.text(d[0] * .75, d[1] * .75 - .45, lab, color=col, fontweight="bold", ha="center")
ax.set(title="Training data; arrow = direction\neach model reads", xlim=(-3.5, 3.5), ylim=(-3.5, 3.5)); ax.set_aspect("equal")
ax.scatter([], [], c=GREEN, label="real"); ax.scatter([], [], c=RED, label="fake")
ax.scatter([], [], c="k", marker="o", label="database A"); ax.scatter([], [], c="k", marker="s", label="database B")
ax.legend(frameon=False, fontsize=8, loc="lower right")

ax = axs[1]
xs = np.arange(2); wd_ = 0.35
ax.bar(xs - wd_ / 2, [h0[-1, 0], h1[-1, 0]], wd_, color=BLUE, label="seen databases (train)")
ax.bar(xs + wd_ / 2, [t0, t1], wd_, color=ORANGE, label="unseen database (test)")
for x_, v_ in zip(np.r_[xs - wd_ / 2, xs + wd_ / 2], [h0[-1, 0], h1[-1, 0], t0, t1]):
    ax.text(x_, v_ + .01, f"{v_:.2f}", ha="center", fontsize=9)
ax.set(xticks=xs, xticklabels=["no DANN", "DANN"], ylim=(0, 1.4), ylabel="real/fake accuracy", title="DANN trades a little train accuracy\nfor better transfer")
ax.legend(frameon=False, fontsize=8, loc="upper center")

ax = axs[2]
ax.plot(h1[:, 0], c=GREEN, label="task head: real/fake")
ax.plot(h1[:, 1], c=ORANGE, label="domain head: which database")
ax.plot(h0[:, 1], c=ORANGE, ls=":", label="domain head, no DANN")
ax.axhline(.5, c=GRAY, ls=":"); ax.text(500, .51, "chance", ha="right", color=GRAY, fontsize=9)
ax.set(xlabel="training step", ylabel="accuracy (train)", title="Domain head accuracy is pushed down", ylim=(.4, 1.25), xlim=(0, 500))
ax.legend(frameon=False, fontsize=8, loc="upper right")
fig.savefig(f"{OUT}/03-toy.png", dpi=150, bbox_inches="tight")
print("no DANN: w", w0.round(2), "train/dom/test", h0[-1].round(2), round(t0, 2))
print("DANN   : w", w1.round(2), "train/dom/test", h1[-1].round(2), round(t1, 2))
