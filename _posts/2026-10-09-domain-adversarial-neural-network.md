---
title: "Domain Adversarial Neural Network (DANN), Explained Simply"
description: "A simple, visual explanation of the Domain Adversarial Neural Network (DANN): the gradient reversal layer, the loss equations, a toy experiment, and how it is used in Nkululeko."
excerpt: "How to stop a model from learning shortcuts like 'this recording style means fake'. A short visual tour of DANN and the gradient reversal layer."
date: 2026-10-09 00:00:00 +0900
mathjax: true
---

Imagine a deepfake detector trained on two databases. Database A has mostly real speech and database B has mostly fake speech. The model may quietly learn: *"this microphone and recording style means real, that one means fake."* On a new database the shortcut breaks, and the detector fails. The same problem appears for emotion recognition across corpora or languages.

A **Domain Adversarial Neural Network (DANN)** (Ganin and Lempitsky, 2015) fights this. The idea in one sentence:

> Train the model to do its task, **and at the same time** make its internal features useless for guessing which database (domain) the audio came from.

I recently saw this added to [Nkululeko in PR #465](https://github.com/felixbur/nkululeko/pull/465), so I use that code as the running example.

## 1. The architecture

<img src="{{ '/images/dann/01-architecture.png' | relative_url }}" alt="DANN architecture with a task head and a domain head behind a gradient reversal layer">

- **Shared model (blue):** turns the audio into a feature vector $$h$$. This is your normal model (MLP, CNN, AASIST, ...).
- **Task head (green):** predicts what you care about, for example real vs. fake.
- **Domain head (orange):** a small extra classifier that predicts the *nuisance* label, for example which database or language the audio came from.
- **GRL (red):** the gradient reversal layer, the one trick that makes it all work. It sits between the features and the domain head.

Both heads are trained at the same time on the same features. The domain head is **only used during training**. At test time you use the task head only.

## 2. The trick: gradient reversal

Normally, a head that predicts domains would push the features to *contain* domain information (that is how it gets its accuracy). We want the opposite. The GRL does this with two simple rules:

<img src="{{ '/images/dann/02-grl.png' | relative_url }}" alt="Gradient reversal layer: identity forward, negated and scaled gradient backward">

| Pass | What the GRL does | Equation |
|---|---|---|
| **Forward** | Nothing. It passes the features through. | $$\mathrm{GRL}(h) = h$$ |
| **Backward** | Flips the sign of the gradient and scales it. | $$\dfrac{\partial\,\mathrm{GRL}}{\partial h} = -\lambda$$ |

So the domain head still learns normally to guess the domain from `h`. But the gradient that travels *back into the shared model* is reversed. The shared model is therefore told: *"change your features so that the domain head becomes worse."* It is a two-player game: the domain head tries to detect the domain, the feature extractor tries to hide it.

Here is the core of it in PyTorch, as in the PR (`nkululeko/models/domain_adversarial.py`):

```python
class _GradientReversalFunction(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x, lambda_):
        ctx.lambda_ = lambda_
        return x.view_as(x)              # identity going forward

    @staticmethod
    def backward(ctx, grad_output):
        return -ctx.lambda_ * grad_output, None   # flip and scale going backward
```

## 3. The equations, annotated

The total loss that the model minimizes is:

$$
L_{\text{total}} = L_{\text{task}} + w \sum_{k} L_{\text{dom},k}
$$

| Symbol | Meaning |
|---|---|
| $$L_{\text{task}}$$ | The usual loss of the main task (cross-entropy for real/fake). |
| $$L_{\text{dom},k}$$ | Cross-entropy of the domain head for the nuisance column `k` (for example `source_db`, `language`). |
| $$\sum_k$$ | You may use several nuisance columns at once. One head is made per column, and the losses are summed. |
| $$w$$ | `dann_weight`: how much the domain loss counts in the total. |

For the feature extractor parameters $$\theta_f$$, the update is:

$$
\theta_f \leftarrow \theta_f - \eta \Big( \underbrace{\frac{\partial L_{\text{task}}}{\partial \theta_f}}_{\text{be good at the task}} - \lambda \underbrace{\frac{\partial L_{\text{dom}}}{\partial \theta_f}}_{\text{be BAD for the domain head}} \Big)
$$

| Symbol | Meaning |
|---|---|
| $$\eta$$ | Learning rate. |
| $$\partial L_{\text{task}} / \partial \theta_f$$ | Normal gradient: make features useful for the task. |
| $$-\lambda \, \partial L_{\text{dom}} / \partial \theta_f$$ | **Reversed** gradient from the GRL: make features *unhelpful* for the domain head. This is the $$-\lambda$$ from the table above. |
| $$\lambda$$ | `dann_lambda`: the strength of the reversal. Too small gives no effect, too large can make training unstable. |

The domain head itself uses the normal (non-reversed) gradient of `L_dom`, so it keeps trying its best. That is what makes the game adversarial.

## 4. A toy experiment

To see the effect, I wrote a tiny DANN by hand in numpy (one linear feature, two logistic heads; this is *not* the Nkululeko code, only an illustration). Real/fake differs along one direction in the 2D input space, and database A/B differs along another. In the **training** data, database B is 85% fake, so "database" is a strong shortcut. In the **unseen test** database the link is reversed (15% fake).

<img src="{{ '/images/dann/03-toy.png' | relative_url }}" alt="Toy DANN experiment: direction read by the model, accuracy on seen and unseen data, domain head accuracy over training">

- **Left:** each arrow is the direction in input space that the model reads. Without DANN (gray) it tilts toward the database axis (the vertical direction), because that helps on the training data. With DANN (blue) it points along the real/fake axis only.
- **Middle:** without DANN, training accuracy is high (0.96) but it drops to 0.85 on the unseen database. With DANN, training accuracy is lower (0.82) but accuracy on the unseen database is **0.96**. DANN gives up the easy shortcut and gets better transfer.
- **Right:** the accuracy of the domain head falls from 0.86 (no DANN, dotted) to 0.69 (DANN). The feature still carries some domain information, but much less.

This matches the usual pattern: a worse score on data you already have, a better score on data you have not seen.

## 5. Using it in Nkululeko

The PR adds DANN to the `aasist`, `mlp`, `mlp_reg`, `cnn` and `adm` models. It is off by default. You turn it on in the `[MODEL]` section of the ini file:

```ini
[MODEL]
type = aasist
dann_columns = ['source_db']   # the nuisance label(s): any column of the training data
dann_lambda = 1.0              # λ: strength of the reversal
dann_weight = 1.0              # w: weight of each domain loss
dann_reverse = True            # False = plain auxiliary head (ablation, no reversal)
```

A few practical notes from the PR:

- `dann_columns` can list several columns, for example `['source_db', 'language']`. Each column gets its own head.
- The head attaches to the last hidden layer (`mlp`, `mlp_reg`, `cnn`), the pooled readout (`aasist`) or the concatenated branch activations (`adm`).
- `dann_reverse = False` removes the reversal. The domain head then becomes an ordinary extra task, which is a useful **ablation** to check whether the adversarial part really helps.
- Classic models such as `svm` and `xgb` ignore these keys, because they have no gradients to reverse.
- The domain heads are not saved with the model. They are only needed for training.
- The PR author reports that on their AASIST experiments, DANN on `source_db` gave a lower EER on the held-out fold than DANN on `language` (16.75% vs. 26.14%). Which nuisance label to remove matters, so try it.

## 6. When it helps, and when it does not

- **It needs a domain label** for each training sample, and at least two different values (the code raises an error otherwise).
- **It does not guarantee invariance.** A strong enough domain head can still find domain traces, as the 0.69 in the toy example shows.
- **It can hurt if the domain really carries signal.** If, say, language truly correlates with the label in your application, removing it will cost accuracy.
- **Tuning matters.** Start with $$\lambda = 1$$, watch the task and domain losses, and compare against the `dann_reverse = False` ablation.

## Summary

DANN = **normal model + a domain classifier on the features + a gradient reversal layer between them.** The classifier tries to guess the domain, and the reversed gradient teaches the features to hide it. The result is features that rely less on database-specific shortcuts and often transfer better to unseen data.

*References: Y. Ganin and V. Lempitsky, "Unsupervised Domain Adaptation by Backpropagation," ICML 2015 ([arXiv:1409.7495](https://arxiv.org/abs/1409.7495)). Implementation: [Nkululeko PR #465](https://github.com/felixbur/nkululeko/pull/465).*

*Figures are generated by [`blogs/dann_figures.py`](https://github.com/bagustris/bagustris.github.io/blob/master/blogs/dann_figures.py).*
