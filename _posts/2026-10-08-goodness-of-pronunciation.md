---
title: "Goodness of Pronunciation (GOP), Explained Simply"
description: "A simple, visual explanation of Goodness of Pronunciation (GOP): how a speech model turns phone posteriors into a pronunciation score, with annotated equations and figures."
excerpt: "How can a computer tell whether you pronounced a sound correctly? A short visual tour of Goodness of Pronunciation (GOP)."
date: 2026-10-08 00:00:00 +0900
---

How can a computer tell whether you said the word *cat* correctly, or whether your "a" sounded more like "e"? **Goodness of Pronunciation (GOP)** is the classic answer. It gives every phone (a single speech sound) a score: *how confident is the model that this sound is the one you were supposed to say?* GOP was introduced by Witt and Young (2000) and is still the base of many pronunciation-training systems today.

## 1. The big picture

1. You read a known text, for example *cat*, which has the target phones **/k/ /æ/ /t/**.
2. **Forced alignment** finds where each phone starts and ends in your audio.
3. An acoustic model gives, for every short frame (about 10 ms), a probability for each possible phone.
4. For each target phone, **average the model's confidence** over its frames. That average is the GOP.

No hand-made rules about "what a wrong /æ/ looks like" are needed. We only ask how much the model believes the right phone was said.

## 2. What the model sees

<img src="{{ '/images/gop/01-posteriors.png' | relative_url }}" alt="Phone posterior heatmaps for a correct and an incorrect pronunciation">

Each column is one time frame and each row is a candidate phone. Darker blue means higher probability, `P(q | frame)`. The dashed lines are the phone boundaries from forced alignment.

- **A (left):** the speaker said /k æ t/. In each segment the dark cells sit on the row of the target phone.
- **B (right):** the speaker said /k e t/. In the middle segment the dark cells moved to the row **e**, while the target row **æ** is almost empty. This is the signal that something went wrong.

(These posteriors are simulated for illustration. A real system gets them from a trained acoustic model.)

## 3. The equation, annotated

This is the simple, widely used **posterior-based** form (as in neural-network GOP). Witt and Young's original compares likelihoods with competing phones, but the idea is the same.

<img src="{{ '/images/gop/03-formula.png' | relative_url }}" alt="The GOP equation with each symbol explained">

In plain text:

```
GOP(p) = (1 / T_p) * sum over t = s..e of  log P(p | o_t)
```

| Symbol | Meaning |
|---|---|
| `p` | The **target phone**, what the speaker *should* say (here /æ/). |
| `s`, `e` | First and last frame of phone `p`, from forced alignment. |
| `T_p` | Number of frames in the phone, `e − s + 1`. Dividing by it is an **average**, so a long phone is not punished just for being long. |
| `o_t` | The audio (acoustic features) at frame `t`. |
| `P(p \| o_t)` | The model's **posterior**: probability that frame `t` is phone `p`. Between 0 and 1. |
| `log` | Turns probabilities into scores. `log 1 = 0` (perfect), and the score drops quickly as the probability goes toward 0. |

How to read the result:

- GOP is **always ≤ 0**.
- **Close to 0** (for example −0.2) means the model is confident, so the pronunciation is good.
- **Very negative** (for example −2) means the model thinks it was some other sound, so it is likely mispronounced.

### Worked example

Suppose /æ/ has 3 frames and the model gives `P(æ | o_t) = 0.9, 0.8, 0.1`. Then

```
GOP = (log 0.9 + log 0.8 + log 0.1) / 3
    = (−0.105 − 0.223 − 2.303) / 3
    ≈ −0.88
```

One bad frame pulled the average down a lot. This is a feature of the log: very unlikely frames are punished heavily.

## 4. From score to decision

<img src="{{ '/images/gop/02-gop-scores.png' | relative_url }}" alt="GOP scores per phone for correct and incorrect speaker">

Compute the GOP of every phone, then compare it with a **threshold** (the dashed line). Below the threshold means "flag as mispronounced".

For the correct speaker, all three phones have GOP around −0.2. For the speaker who said /e/ instead of /æ/, /k/ and /t/ are still fine, but **/æ/ drops to about −2.1**, far below the threshold. The system can now say exactly *which* sound to fix, not just "your pronunciation is bad".

The threshold is not universal. It is usually tuned per phone on data labelled by human experts, because some phones are naturally harder for the model than others.

## 5. A common improvement: compare with the best competitor

A low GOP can also happen when the audio is noisy, even if the phone is right. A popular variant, the **Log Posterior Ratio (LPR)**, asks a sharper question: *is the target phone better than the best alternative?*

```
LPR(p) = GOP(p) − max over q ≠ p of GOP(q)
```

- `GOP(p)`: the score of the target phone.
- `max GOP(q)`: the score of the strongest competing phone (here, `e`).
- **Positive** LPR: the target wins. **Negative** LPR: another phone wins, so the speaker likely said that other phone.

In the example above, LPR for /æ/ is about +3.0 for the correct speaker and about **−1.8** for the speaker who said /e/. Noise lowers all the scores together, so LPR is less affected by it. It also tells you *what* the speaker probably said instead.

## 6. Limits to keep in mind

- **Forced alignment must be right.** If the boundaries are wrong, the frames are wrong, and so is the score.
- **Native accents vary.** A model trained mostly on one accent may score valid accents too low.
- **A single number per phone is coarse.** Modern systems feed GOP features (and the LPR) into a small classifier, or train neural models end to end, but GOP is still the standard baseline to compare against.

## Summary

GOP = **the average log probability that the model assigns to the phone you were supposed to say.** Close to 0 means good, very negative means suspicious. Add a threshold to get a decision, and a competitor comparison (LPR) to get a more robust one.

*Reference: S. M. Witt and S. J. Young, "Phone-level pronunciation scoring and assessment for interactive language learning," Speech Communication, 30(2–3), 2000.*

*Figures are generated by [`blogs/gop_figures.py`](https://github.com/bagustris/bagustris.github.io/blob/master/blogs/gop_figures.py).*
