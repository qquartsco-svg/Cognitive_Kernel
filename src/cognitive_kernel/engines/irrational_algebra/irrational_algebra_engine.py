"""
Irrational Algebra Engine

상태 벡터의 비율 구조를 무리수 공명으로 읽고,
대수적 불변식 잔차를 계산해 구조 건강도를 반환한다.
"""

from __future__ import annotations

import math
from typing import Iterable, List, Optional, Sequence

from .config import IrrationalAlgebraConfig
from .models import (
    AlgebraicInvariant,
    IrrationalAlgebraSnapshot,
    IrrationalConstant,
    IrrationalObservation,
)


class IrrationalAlgebraEngine:
    """무리수-대수학 기반 구조 분석 엔진."""

    def __init__(self, config: Optional[IrrationalAlgebraConfig] = None):
        self.config = config or IrrationalAlgebraConfig()
        self._constants = [
            IrrationalConstant("pi", math.pi, "transcendental", "boundary/rotation"),
            IrrationalConstant("sqrt2", math.sqrt(2.0), "algebraic", "diagonal/stretch"),
            IrrationalConstant("phi", (1.0 + math.sqrt(5.0)) / 2.0, "algebraic", "growth/hierarchy"),
            IrrationalConstant("e", math.e, "transcendental", "continuous growth"),
        ]

    def catalog(self) -> List[IrrationalConstant]:
        return list(self._constants)

    def analyze(
        self,
        values: Sequence[float],
        *,
        observer_omega: Optional[float] = None,
        boundary_mismatch: Optional[float] = None,
        dynamic_health: Optional[float] = None,
    ) -> IrrationalAlgebraSnapshot:
        """비율 구조와 대수적 닫힘 정도를 분석한다.

        Args:
            values:          상태 벡터 (크기 기반 비율 분석)
            observer_omega:  Observer 시스템의 Ω 스코어 (0~1)
            boundary_mismatch: BoundaryConvergenceEngine의 mismatch 값
            dynamic_health:  convergence_dynamics.health_from_dynamics()
                             결과값 (0~1). None이면 0.5 (중립) 적용.
        """
        magnitudes = [abs(float(v)) for v in values if abs(float(v)) > self.config.min_scale]
        ratios = self._derive_ratios(magnitudes)
        observations = [self._observe_ratio(r) for r in ratios]
        dominant = max(observations, key=lambda item: item.score).name if observations else "none"
        resonance_score = self._average([obs.score for obs in observations], default=0.0)

        invariants = self._build_invariants(observations)
        algebraic_closure = self._average(
            [1.0 - min(1.0, inv.residual) for inv in invariants],
            default=0.0,
        )

        boundary_alignment = self._boundary_alignment(boundary_mismatch)
        observer_alignment = self._clamp(observer_omega if observer_omega is not None else 0.5)
        dynamics_alignment = self._clamp(dynamic_health if dynamic_health is not None else 0.5)

        structural_health = self._clamp(
            self.config.ratio_weight     * resonance_score
            + self.config.invariant_weight * algebraic_closure
            + self.config.boundary_weight  * boundary_alignment
            + self.config.observer_weight  * observer_alignment
            + self.config.dynamics_weight  * dynamics_alignment
        )

        metadata = {
            "ratio_count":      float(len(ratios)),
            "dominant_score":   max((obs.score for obs in observations), default=0.0),
            "dynamic_health":   dynamics_alignment,
        }

        return IrrationalAlgebraSnapshot(
            dominant_constant=dominant,
            resonance_score=resonance_score,
            algebraic_closure=algebraic_closure,
            boundary_alignment=boundary_alignment,
            observer_alignment=observer_alignment,
            structural_health=structural_health,
            observations=observations,
            invariants=invariants,
            metadata=metadata,
        )

    def _derive_ratios(self, magnitudes: Sequence[float]) -> List[float]:
        if len(magnitudes) < 2:
            return []
        ratios: List[float] = []
        for left, right in zip(magnitudes, magnitudes[1:]):
            if right > self.config.ratio_epsilon:
                ratios.append(max(left, right) / min(left, right))
        return ratios

    def _observe_ratio(self, ratio: float) -> IrrationalObservation:
        best = None
        best_deviation = float("inf")
        for constant in self._constants:
            deviation = abs(ratio - constant.value) / constant.value
            if deviation < best_deviation:
                best = constant
                best_deviation = deviation
        assert best is not None
        score = math.exp(-best_deviation / self.config.resonance_temperature)
        return IrrationalObservation(
            name=best.name,
            observed_ratio=ratio,
            target_value=best.value,
            deviation=best_deviation,
            score=self._clamp(score),
        )

    def _build_invariants(
        self,
        observations: Sequence[IrrationalObservation],
    ) -> List[AlgebraicInvariant]:
        by_name = {obs.name: obs.observed_ratio for obs in observations}
        invariants: List[AlgebraicInvariant] = []

        if "phi" in by_name:
            ratio = by_name["phi"]
            residual = abs(ratio * ratio - ratio - 1.0)
            invariants.append(
                AlgebraicInvariant(
                    name="phi_quadratic",
                    residual=residual,
                    satisfied=residual <= self.config.invariant_tolerance,
                    expression="x^2 - x - 1 = 0",
                )
            )
        if "sqrt2" in by_name:
            ratio = by_name["sqrt2"]
            residual = abs(ratio * ratio - 2.0)
            invariants.append(
                AlgebraicInvariant(
                    name="sqrt2_quadratic",
                    residual=residual,
                    satisfied=residual <= self.config.invariant_tolerance,
                    expression="x^2 - 2 = 0",
                )
            )
        if "pi" in by_name:
            ratio = by_name["pi"]
            residual = abs(math.sin(ratio))
            invariants.append(
                AlgebraicInvariant(
                    name="pi_rotational_closure",
                    residual=residual,
                    satisfied=residual <= 0.05,
                    expression="sin(x) ~= 0 near rotational closure",
                )
            )
        if "e" in by_name:
            ratio = by_name["e"]
            residual = abs(math.log(max(ratio, self.config.ratio_epsilon)) - 1.0)
            invariants.append(
                AlgebraicInvariant(
                    name="e_log_fixed_point",
                    residual=residual,
                    satisfied=residual <= 0.05,
                    expression="ln(x) ~= 1",
                )
            )
        return invariants

    def _boundary_alignment(self, boundary_mismatch: Optional[float]) -> float:
        if boundary_mismatch is None:
            return 0.5
        mismatch = max(0.0, float(boundary_mismatch))
        return 1.0 / (1.0 + mismatch)

    @staticmethod
    def _clamp(value: float) -> float:
        return max(0.0, min(1.0, float(value)))

    @staticmethod
    def _average(values: Iterable[float], *, default: float) -> float:
        items = list(values)
        if not items:
            return default
        return sum(items) / len(items)
