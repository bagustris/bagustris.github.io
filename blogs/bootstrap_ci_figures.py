"""Generate figures for the post "Bootstrap Confidence Interval, Explained with Pictures"."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "images/bootstrap"
rng = np.random.default_rng(42)
B = 10000
BLUE, RED, GRAY, GREEN = "#2b6cb0", "#c53030", "#718096", "#2f855a"
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})


def boot_mean(x, B=B):
    idx = rng.integers(0, len(x), (B, len(x)))
    return x[idx].mean(axis=1)


def ci(a):
    return np.percentile(a, [2.5, 97.5])


# ---- Fig 1: the idea -------------------------------------------------
x = rng.normal(70, 10, 20).round(1)
fig, ax = plt.subplots(1, 3, figsize=(13, 3.8), gridspec_kw={"width_ratios": [1, 1.1, 1.6]})
ax[0].eventplot(x, colors=BLUE, lineoffsets=0, linelengths=0.6)
ax[0].axvline(x.mean(), color=RED, lw=2)
ax[0].set(yticks=[], title="1. Our one sample (n=20)", xlabel="score")
ax[0].annotate(f"mean = {x.mean():.1f}", (x.mean(), 0.3), (x.mean() + 4, 0.55), color=RED,
               arrowprops=dict(arrowstyle="->", color=RED))
ax[0].set_ylim(-0.5, 0.9)
for i, c in enumerate([BLUE, GREEN, GRAY]):
    rs = rng.choice(x, len(x), replace=True)
    ax[1].eventplot(rs, colors=c, lineoffsets=i, linelengths=0.6)
    ax[1].plot(rs.mean(), i + 0.45, "v", color=RED)
ax[1].set(yticks=[0, 1, 2], yticklabels=["resample 3", "resample 2", "resample 1"][::-1],
          title="2. Draw n values WITH replacement,\n   compute the mean. Repeat.", xlabel="score")
ax[1].text(0.02, 0.97, "red ▼ = mean of each resample", transform=ax[1].transAxes, va="top", color=RED, fontsize=9)
bm = boot_mean(x)
lo, hi = ci(bm)
ax[2].hist(bm, bins=60, color="#bee3f8", edgecolor="white")
ax[2].axvspan(lo, hi, color=BLUE, alpha=0.15)
for v in (lo, hi):
    ax[2].axvline(v, color=BLUE, lw=2, ls="--")
ax[2].set(title=f"3. Do it {B:,} times → distribution of means", xlabel="resampled mean", yticks=[])
top = ax[2].get_ylim()[1]
ax[2].annotate(f"2.5th percentile\n{lo:.1f}", (lo, top * .6), (lo - 4.5, top * .85), arrowprops=dict(arrowstyle="->"))
ax[2].annotate(f"97.5th percentile\n{hi:.1f}", (hi, top * .6), (hi + 0.4, top * .85), arrowprops=dict(arrowstyle="->"))
ax[2].text((lo + hi) / 2, top * .35, "middle 95%\n= 95% CI", ha="center", color=BLUE, fontweight="bold")
fig.tight_layout()
fig.savefig(f"{OUT}/01-bootstrap-idea.png", dpi=130)
plt.close(fig)

# ---- Fig 2: include / exclude zero ----------------------------------
n = 25
z = rng.normal(0, 1, n)
z = (z - z.mean()) / z.std(ddof=1)  # fix mean/SD exactly so the example is deterministic
cases = [("A: CI includes 0  →  not significant", 0.3 + 1.0 * z, RED),
         ("B: CI excludes 0  →  significant", 1.0 + 1.0 * z, GREEN)]
fig, axs = plt.subplots(1, 2, figsize=(12, 3.9), sharex=True)
for a, (t, d, c) in zip(axs, cases):
    bm = boot_mean(d)
    lo, hi = ci(bm)
    a.hist(bm, bins=60, color=c, alpha=0.3, edgecolor="white")
    a.axvline(0, color="black", lw=2)
    a.axvline(lo, color=c, ls="--", lw=2)
    a.axvline(hi, color=c, ls="--", lw=2)
    top = a.get_ylim()[1]
    a.annotate("zero = 'no effect'", (0, top * .55), (-1.0 if lo < 0 else -1.1, top * .8),
               arrowprops=dict(arrowstyle="->"))
    a.text((lo + hi) / 2, top * .35, f"95% CI\n[{lo:.2f}, {hi:.2f}]", ha="center", color=c, fontweight="bold", bbox=dict(fc="white", ec=c, alpha=.9))
    a.set(title=t, xlabel="bootstrapped mean difference", yticks=[])
    a.set_xlim(-1.4, 2.0)
fig.tight_layout()
fig.savefig(f"{OUT}/02-include-exclude-zero.png", dpi=130)
plt.close(fig)

# ---- Fig 3: paired vs unpaired --------------------------------------
n = 20
subj = rng.normal(70, 12, n)            # big person-to-person differences
before = subj + rng.normal(0, 2, n)
after = subj + 3 + rng.normal(0, 2, n)  # small consistent gain (~3)
d = after - before
fig, axs = plt.subplots(1, 3, figsize=(14, 4.2), gridspec_kw={"width_ratios": [1, 1.3, 1.3]})
for b_, a_ in zip(before, after):
    axs[0].plot([0, 1], [b_, a_], "-o", color=GRAY, alpha=0.6, ms=4)
axs[0].set(xticks=[0, 1], xticklabels=["before", "after"], title="Same 20 people, measured twice",
           ylabel="score")
axs[0].text(0.5, before.min() - 2, "lines go up almost in parallel", ha="center", color=GREEN, fontsize=9)

pd_ = boot_mean(d)
plo, phi = ci(pd_)
idx = rng.integers(0, n, (B, n))
ud = after[rng.integers(0, n, (B, n))].mean(1) - before[rng.integers(0, n, (B, n))].mean(1)
ulo, uhi = ci(ud)
for a, arr, c, lo_, hi_, t in [(axs[1], pd_, GREEN, plo, phi, "Paired: resample the differences"),
                               (axs[2], ud, RED, ulo, uhi, "Unpaired: resample the groups separately")]:
    a.hist(arr, bins=np.linspace(-15, 15, 120), color=c, alpha=0.3, edgecolor="white")
    a.axvline(0, color="black", lw=2)
    a.axvline(lo_, color=c, ls="--", lw=2)
    a.axvline(hi_, color=c, ls="--", lw=2)
    top = a.get_ylim()[1]
    a.text((lo_ + hi_) / 2, top * .45, f"95% CI [{lo_:.1f}, {hi_:.1f}]\nwidth = {hi_ - lo_:.1f}",
               ha="center", color=c, fontweight="bold", bbox=dict(fc="white", ec=c, alpha=.9))
    a.text(0.3, top * .93, "0 = no effect", va="top")
    a.set(title=t, xlabel="mean difference (after − before)", yticks=[])
    a.set_xlim(-15, 15)
fig.tight_layout()
fig.savefig(f"{OUT}/03-paired-vs-unpaired.png", dpi=130)
plt.close(fig)
print("paired CI", plo, phi, "unpaired CI", ulo, uhi)
