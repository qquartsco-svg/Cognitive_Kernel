"""
Irrational Algebra Engine Configuration
"""

from dataclasses import dataclass


@dataclass
class IrrationalAlgebraConfig:
    """무리수-대수학 엔진 설정.

    가중치 합 = 1.0:
      ratio_weight + invariant_weight + boundary_weight
      + observer_weight + dynamics_weight = 1.0
    dynamics_weight > 0 이면 convergence_dynamics 연동 활성화.
    """

    ratio_epsilon: float = 1e-9
    invariant_tolerance: float = 1e-6
    resonance_temperature: float = 1.0
    # structural health 가중치 (합 = 1.0)
    observer_weight: float = 0.15
    boundary_weight: float = 0.20
    invariant_weight: float = 0.25
    ratio_weight: float = 0.25
    dynamics_weight: float = 0.15   # convergence_dynamics 연동 가중치
    min_scale: float = 1e-9

    def __post_init__(self) -> None:
        if self.ratio_epsilon <= 0:
            raise ValueError("ratio_epsilon must be positive")
        if self.invariant_tolerance <= 0:
            raise ValueError("invariant_tolerance must be positive")
        if self.resonance_temperature <= 0:
            raise ValueError("resonance_temperature must be positive")
        total = (self.ratio_weight + self.invariant_weight
                 + self.boundary_weight + self.observer_weight
                 + self.dynamics_weight)
        if abs(total - 1.0) > 1e-6:
            raise ValueError(f"가중치 합이 1.0이 아닙니다: {total:.6f}")
