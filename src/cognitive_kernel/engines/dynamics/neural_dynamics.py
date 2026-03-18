"""Neural Dynamics Core (Continuous-Time)

This module provides a minimal continuous-time neural dynamics core.

Canonical form (common in computational neuroscience / rate networks):

    τ * dx/dt = -x + f(Wx + I + b)

Where:
- x: state vector (membrane potential / rate state)
- W: recurrent weight matrix
- I: external input
- b: bias
- f: nonlinearity
- τ: time constant

Design goals:
- Minimal (pure Python, no heavy deps)
- Deterministic-by-default (noise_scale=0)
- Easy to observe attractors / convergence under continuous-time dynamics

Author: GNJz (Qquarts)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional, Sequence
import math
import random

Vector = List[float]
Matrix = List[List[float]]


def _tanh(x: float) -> float:
    return math.tanh(x)


def _sigmoid(x: float) -> float:
    # numerically safer sigmoid
    if x >= 0.0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def _relu(x: float) -> float:
    return x if x > 0.0 else 0.0


def get_activation(name: str) -> Callable[[float], float]:
    n = name.lower().strip()
    if n in ("tanh",):
        return _tanh
    if n in ("sigmoid", "logistic"):
        return _sigmoid
    if n in ("relu",):
        return _relu
    if n in ("linear", "identity"):
        return lambda v: v
    raise ValueError(f"Unknown activation: {name}")


@dataclass
class ContinuousDynamicsConfig:
    """Configuration for continuous-time dynamics."""

    dt: float = 0.01
    tau: float = 0.1
    activation: str = "tanh"

    # Euler-Maruyama diffusion scale (0 = deterministic)
    noise_scale: float = 0.0

    # optional clipping for numerical safety
    clip_state: Optional[float] = None  # if set, clip x to [-clip, clip]

    def validate(self) -> None:
        if self.dt <= 0.0:
            raise ValueError("dt must be > 0")
        if self.tau <= 0.0:
            raise ValueError("tau must be > 0")
        if self.noise_scale < 0.0:
            raise ValueError("noise_scale must be >= 0")
        if self.clip_state is not None and self.clip_state <= 0.0:
            raise ValueError("clip_state must be > 0 when provided")


class NeuralDynamicsCore:
    """Minimal continuous-time recurrent dynamics simulator."""

    def __init__(
        self,
        W: Matrix,
        b: Optional[Sequence[float]] = None,
        config: Optional[ContinuousDynamicsConfig] = None,
        seed: Optional[int] = None,
    ):
        self.config = config or ContinuousDynamicsConfig()
        self.config.validate()

        if seed is not None:
            random.seed(seed)

        self.W: Matrix = [list(row) for row in W]
        self.n: int = len(self.W)
        if self.n == 0:
            raise ValueError("W must be non-empty")
        if any(len(row) != self.n for row in self.W):
            raise ValueError("W must be a square matrix")

        if b is None:
            self.b = [0.0 for _ in range(self.n)]
        else:
            if len(b) != self.n:
                raise ValueError("bias vector b must have length n")
            self.b = list(b)

        self.f = get_activation(self.config.activation)

    def _matvec(self, x: Sequence[float]) -> Vector:
        out = [0.0] * self.n
        for i in range(self.n):
            s = 0.0
            wi = self.W[i]
            for j in range(self.n):
                s += wi[j] * x[j]
            out[i] = s
        return out

    def step(
        self,
        x: Sequence[float],
        I: Optional[Sequence[float]] = None,
    ) -> Vector:
        """One Euler-Maruyama step."""
        if len(x) != self.n:
            raise ValueError("x must have length n")
        if I is None:
            I_vec = [0.0] * self.n
        else:
            if len(I) != self.n:
                raise ValueError("I must have length n")
            I_vec = list(I)

        Wx = self._matvec(x)
        u = [Wx[i] + I_vec[i] + self.b[i] for i in range(self.n)]
        fx = [self.f(u[i]) for i in range(self.n)]

        dt = self.config.dt
        tau = self.config.tau
        k = dt / tau

        x_next = [0.0] * self.n
        for i in range(self.n):
            drift = -x[i] + fx[i]
            v = x[i] + k * drift

            if self.config.noise_scale > 0.0:
                v += random.gauss(0.0, self.config.noise_scale * math.sqrt(dt))

            if self.config.clip_state is not None:
                c = self.config.clip_state
                if v > c:
                    v = c
                elif v < -c:
                    v = -c

            x_next[i] = v

        return x_next

    def run(
        self,
        x0: Sequence[float],
        steps: int,
        input_schedule: Optional[Callable[[int], Sequence[float]]] = None,
        stop_tol: Optional[float] = None,
        return_trajectory: bool = True,
    ):
        """Run dynamics for a fixed number of steps.

        Args:
            x0: initial state
            steps: number of integration steps
            input_schedule: optional callable mapping step_idx -> I vector
            stop_tol: stop early when ||x_{t+1}-x_t||_inf < stop_tol
            return_trajectory: if True returns list of x; else returns final x
        """
        if steps <= 0:
            raise ValueError("steps must be > 0")

        x = list(x0)
        if len(x) != self.n:
            raise ValueError("x0 must have length n")

        traj = [list(x)] if return_trajectory else None

        for t in range(steps):
            I = input_schedule(t) if input_schedule is not None else None
            x_next = self.step(x, I=I)

            if stop_tol is not None:
                delta = max(abs(x_next[i] - x[i]) for i in range(self.n))
                if delta < stop_tol:
                    x = x_next
                    if return_trajectory:
                        traj.append(list(x))
                    break

            x = x_next
            if return_trajectory:
                traj.append(list(x))

        return traj if return_trajectory else x

    def hopfield_energy(self, x: Sequence[float]) -> float:
        """Optional energy for symmetric W (Hopfield-style, rate-coded).

        Note: meaningful primarily when W is symmetric and f is monotone.
        """
        if len(x) != self.n:
            raise ValueError("x must have length n")
        e = 0.0
        for i in range(self.n):
            for j in range(self.n):
                e += x[i] * self.W[i][j] * x[j]
        e *= -0.5
        for i in range(self.n):
            e -= self.b[i] * x[i]
        return e


