"""Plasticity rules for continuous dynamics.

This module intentionally starts minimal:
- Hebbian (rate-based) update with optional weight decay + clipping.

It is meant to connect the continuous-time dynamics core to learning/adaptation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence, Optional

Matrix = List[List[float]]


@dataclass
class HebbianPlasticityConfig:
    """Hebbian plasticity configuration."""

    eta: float = 0.01  # learning rate
    weight_decay: float = 0.0  # L2-like decay on weights
    clip_weight: Optional[float] = None  # if set, clip weights to [-clip, clip]

    def validate(self) -> None:
        if self.eta <= 0.0:
            raise ValueError("eta must be > 0")
        if self.weight_decay < 0.0:
            raise ValueError("weight_decay must be >= 0")
        if self.clip_weight is not None and self.clip_weight <= 0.0:
            raise ValueError("clip_weight must be > 0 when provided")


def hebbian_update(
    W: Matrix,
    pre: Sequence[float],
    post: Optional[Sequence[float]] = None,
    config: Optional[HebbianPlasticityConfig] = None,
) -> Matrix:
    """Apply a single Hebbian update: Δw_ij = η * pre_i * post_j - decay*w_ij.

    Args:
        W: weight matrix (n x n)
        pre: presynaptic activity vector (length n)
        post: postsynaptic activity vector (length n). If None, uses pre (symmetric).
        config: HebbianPlasticityConfig

    Returns:
        Updated weight matrix (new copy).
    """
    cfg = config or HebbianPlasticityConfig()
    cfg.validate()

    n = len(W)
    if n == 0 or any(len(row) != n for row in W):
        raise ValueError("W must be a non-empty square matrix")
    if len(pre) != n:
        raise ValueError("pre must have length n")
    if post is None:
        post_vec = list(pre)
    else:
        if len(post) != n:
            raise ValueError("post must have length n")
        post_vec = list(post)

    eta = cfg.eta
    decay = cfg.weight_decay

    W_new: Matrix = [list(row) for row in W]
    for i in range(n):
        for j in range(n):
            dw = eta * pre[i] * post_vec[j]
            if decay > 0.0:
                dw -= decay * W_new[i][j]
            W_new[i][j] += dw

    if cfg.clip_weight is not None:
        c = cfg.clip_weight
        for i in range(n):
            for j in range(n):
                v = W_new[i][j]
                if v > c:
                    v = c
                elif v < -c:
                    v = -c
                W_new[i][j] = v

    return W_new


