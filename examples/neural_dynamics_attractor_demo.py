"""
Neural Dynamics Attractor Demo

Goal:
- Observe attractor formation / convergence in a minimal continuous-time network
- Apply a pulse input and see how the system transitions
- Optionally apply a minimal Hebbian plasticity update

Core equation:
    τ * dx/dt = -x + f(Wx + I + b)
"""

import sys
from pathlib import Path

# Add project src to path (demo-friendly)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from cognitive_kernel.engines.dynamics import (
    ContinuousDynamicsConfig,
    NeuralDynamicsCore,
    HebbianPlasticityConfig,
    hebbian_update,
)


def main() -> None:
    # A tiny symmetric network (Hopfield-ish) that tends to settle into stable states.
    W = [
        [1.6, -1.2],
        [-1.2, 1.6],
    ]
    b = [0.0, 0.0]

    cfg = ContinuousDynamicsConfig(dt=0.01, tau=0.1, activation="tanh", noise_scale=0.0, clip_state=5.0)
    core = NeuralDynamicsCore(W=W, b=b, config=cfg, seed=7)

    print("=== Case A: converge from x0 = [0.7, -0.4] ===")
    traj_a = core.run([0.7, -0.4], steps=4000, stop_tol=1e-7, return_trajectory=True)
    xa = traj_a[-1]
    print("final x:", [round(v, 6) for v in xa])
    print("energy (if symmetric):", round(core.hopfield_energy(xa), 6))
    print("steps:", len(traj_a) - 1)

    print("\n=== Case B: converge from x0 = [-0.6, 0.6] ===")
    traj_b = core.run([-0.6, 0.6], steps=4000, stop_tol=1e-7, return_trajectory=True)
    xb = traj_b[-1]
    print("final x:", [round(v, 6) for v in xb])
    print("energy (if symmetric):", round(core.hopfield_energy(xb), 6))
    print("steps:", len(traj_b) - 1)

    print("\n=== Case C: pulse input to push trajectory ===")
    def pulse(t: int):
        # pulse neuron 0 between steps [800, 1400)
        if 800 <= t < 1400:
            return [1.2, 0.0]
        return [0.0, 0.0]

    traj_c = core.run([0.2, 0.2], steps=3000, input_schedule=pulse, stop_tol=None, return_trajectory=True)
    xc = traj_c[-1]
    print("final x:", [round(v, 6) for v in xc])
    print("energy (if symmetric):", round(core.hopfield_energy(xc), 6))

    print("\n=== Optional: minimal Hebbian plasticity (few updates) ===")
    Wp = [row[:] for row in W]
    plastic_cfg = HebbianPlasticityConfig(eta=0.02, weight_decay=0.001, clip_weight=2.0)
    x = [0.5, -0.3]
    core_p = NeuralDynamicsCore(W=Wp, b=b, config=cfg, seed=7)
    for t in range(2000):
        x = core_p.step(x, I=[0.0, 0.0])
        # update every 50 steps
        if t > 0 and t % 50 == 0:
            Wp = hebbian_update(core_p.W, pre=x, post=None, config=plastic_cfg)
            core_p.W = Wp
    print("final x:", [round(v, 6) for v in x])
    print("final W:")
    for row in core_p.W:
        print(" ", [round(v, 4) for v in row])


if __name__ == "__main__":
    main()


