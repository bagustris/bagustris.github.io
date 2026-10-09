"""Generate figures for the post "Goodness of Pronunciation (GOP), Explained Simply"."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "images/gop"
rng = np.random.default_rng(3)
BLUE, RED, GRAY, GREEN = "#2b6cb0", "#c53030", "#718096", "#2f855a"
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})

PH = ["k", "æ", "e", "t"]            # candidate phones (rows)
TARGET = ["k", "æ", "t"]             # canonical phones of "cat"
SEG = [(0, 8), (8, 18), (18, 25)]    # forced-alignment frames of each target phone
T = 25


def posteriors(spoken):
    """Fake frame-level phone posteriors P(q | o_t). `spoken` = what was really said."""
    P = np.zeros((len(PH), T))
    for (s, e), ph in zip(SEG, spoken):
        for t in range(s, e):
            logit = rng.normal(0, 0.5, len(PH))
            logit[PH.index(ph)] += 3.0
            if ph == "e":                      # /e/ is close to /æ/, so some confusion
                logit[PH.index("æ")] += 1.4
            P[:, t] = np.exp(logit) / np.exp(logit).sum()
    return P


def gop(P):
    """Per target phone: GOP (mean log posterior of target) and LPR (vs best competitor)."""
    out = []
    for (s, e), ph in zip(SEG, TARGET):
        i = PH.index(ph)
        lp = np.log(P[:, s:e]).mean(axis=1)    # mean log-posterior of each candidate over the segment
        gop_ = lp[i]
        lpr = gop_ - np.delete(lp, i).max()
        out.append((gop_, lpr))
    return out


good, bad = posteriors(["k", "æ", "t"]), posteriors(["k", "e", "t"])

# ---- Fig 1: posterior heatmaps ---------------------------------------
fig, axs = plt.subplots(1, 2, figsize=(11, 3.6), sharey=True)
for ax, P, ttl in zip(axs, [good, bad], ["A. Said /k æ t/ (correct)", "B. Said /k e t/ (æ → e error)"]):
    im = ax.imshow(P, aspect="auto", cmap="Blues", vmin=0, vmax=1, origin="upper")
    ax.set_yticks(range(len(PH)), PH)
    ax.set_xlabel("time (frames)")
    ax.set_title(ttl, pad=22)
    for (s, e), ph in zip(SEG, TARGET):
        ax.axvline(s - 0.5, color=GRAY, lw=1, ls="--")
        ax.text((s + e - 1) / 2, -0.75, f"/{ph}/", ha="center", color=RED, fontweight="bold")
    ax.axvline(T - 0.5, color=GRAY, lw=1, ls="--")
    ax.spines[["left", "bottom"]].set_visible(False)
axs[0].set_ylabel("candidate phone q")
fig.colorbar(im, ax=axs, label="P(q | frame)", fraction=0.025, pad=0.02)
fig.savefig(f"{OUT}/01-posteriors.png", dpi=150, bbox_inches="tight")

# ---- Fig 2: GOP per phone --------------------------------------------
G, B = gop(good), gop(bad)
fig, ax = plt.subplots(figsize=(7, 3.8))
x = np.arange(3)
w = 0.36
ax.bar(x - w / 2, [g for g, _ in G], w, color=GREEN, label="correct speaker")
ax.bar(x + w / 2, [g for g, _ in B], w, color=RED, label="speaker with æ → e")
thr = -1.0
ax.axhline(thr, color="k", ls="--", lw=1)
ax.text(2.55, thr + 0.05, "threshold", ha="right", va="bottom", fontsize=9)
ax.set_xticks(x, [f"/{p}/" for p in TARGET])
ax.set_ylabel("GOP = mean log P(target | frames)")
ax.set_title("Higher (closer to 0) = better pronounced")
ax.legend(loc="lower left", frameon=False)
fig.savefig(f"{OUT}/02-gop-scores.png", dpi=150, bbox_inches="tight")

# ---- Fig 3: formula anatomy (worked numbers) -------------------------
fig, ax = plt.subplots(figsize=(10, 2.8))
ax.axis("off")
ax.text(0.5, 0.80, r"$\mathrm{GOP}(p)=\frac{1}{T_p}\sum_{t=s}^{e}\log P(p\mid o_t)$",
        ha="center", fontsize=24)
notes = [
    (0.10, r"$p$", "target phone\n(what it should be)"),
    (0.30, r"$T_p$", "number of frames\nin the phone"),
    (0.50, r"$s,\,e$", "start / end frame\n(from forced alignment)"),
    (0.70, r"$o_t$", "acoustic frame\nat time $t$"),
    (0.90, r"$P(p\mid o_t)$", "model's confidence that\nframe $t$ is phone $p$"),
]
for xx, sym, txt in notes:
    ax.text(xx, 0.45, sym, ha="center", fontsize=16, color=BLUE)
    ax.text(xx, 0.25, txt, ha="center", va="center", fontsize=10)
fig.savefig(f"{OUT}/03-formula.png", dpi=150, bbox_inches="tight")

print("GOP good:", [round(g, 2) for g, _ in G], "LPR", [round(l, 2) for _, l in G])
print("GOP bad :", [round(g, 2) for g, _ in B], "LPR", [round(l, 2) for _, l in B])
