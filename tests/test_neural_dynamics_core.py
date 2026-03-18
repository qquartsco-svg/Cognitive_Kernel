"""
Neural dynamics core tests (continuous-time).

We test:
- basic convergence with stop_tol
- input pulse affects trajectory
- Hebbian plasticity updates weights as expected
"""

import sys
from pathlib import Path

import pytest

# 프로젝트 루트를 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from cognitive_kernel.engines.dynamics import (
    ContinuousDynamicsConfig,
    NeuralDynamicsCore,
    HebbianPlasticityConfig,
    hebbian_update,
)


def test_convergence_stop_tol():
    W = [
        [1.6, -1.2],
        [-1.2, 1.6],
    ]
    cfg = ContinuousDynamicsConfig(dt=0.01, tau=0.1, activation="tanh", noise_scale=0.0)
    core = NeuralDynamicsCore(W=W, b=[0.0, 0.0], config=cfg, seed=123)

    traj = core.run([0.7, -0.4], steps=5000, stop_tol=1e-7, return_trajectory=True)
    assert len(traj) >= 2

    # should be close to a fixed point at end
    x_last = traj[-1]
    x_prev = traj[-2]
    delta_inf = max(abs(x_last[i] - x_prev[i]) for i in range(2))
    assert delta_inf < 1e-6


def test_pulse_input_changes_final_state():
    W = [
        [1.6, -1.2],
        [-1.2, 1.6],
    ]
    cfg = ContinuousDynamicsConfig(dt=0.01, tau=0.1, activation="tanh", noise_scale=0.0)
    core = NeuralDynamicsCore(W=W, b=[0.0, 0.0], config=cfg, seed=7)

    x0 = [0.2, 0.2]
    no_pulse_final = core.run(x0, steps=3000, input_schedule=None, stop_tol=None, return_trajectory=False)

    def pulse(t: int):
        if 800 <= t < 1400:
            return [1.2, 0.0]
        return [0.0, 0.0]

    pulse_final = core.run(x0, steps=3000, input_schedule=pulse, stop_tol=None, return_trajectory=False)

    # not asserting exact numbers; just that the pulse induces a noticeable difference
    diff = max(abs(pulse_final[i] - no_pulse_final[i]) for i in range(2))
    assert diff > 1e-3


def test_hebbian_update_changes_weights_and_respects_clip():
    W = [
        [0.0, 0.0],
        [0.0, 0.0],
    ]
    pre = [1.0, -1.0]
    cfg = HebbianPlasticityConfig(eta=0.5, weight_decay=0.0, clip_weight=0.2)

    W2 = hebbian_update(W, pre=pre, post=None, config=cfg)

    # clip should bound values
    for i in range(2):
        for j in range(2):
            assert -0.2 <= W2[i][j] <= 0.2

    # should not be identical to original
    assert any(W2[i][j] != W[i][j] for i in range(2) for j in range(2))


