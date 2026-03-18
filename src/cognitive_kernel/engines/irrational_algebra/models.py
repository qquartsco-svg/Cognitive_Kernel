"""
Irrational Algebra Engine Models
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class IrrationalConstant:
    """무리수 또는 초월수 상수 정의."""

    name: str
    value: float
    family: str
    note: str = ""


@dataclass(frozen=True)
class IrrationalObservation:
    """상태 비율이 특정 무리수에 얼마나 가까운지 기록."""

    name: str
    observed_ratio: float
    target_value: float
    deviation: float
    score: float


@dataclass(frozen=True)
class AlgebraicInvariant:
    """대수적 불변식 잔차."""

    name: str
    residual: float
    satisfied: bool
    expression: str


@dataclass
class IrrationalAlgebraSnapshot:
    """무리수/대수학 레이어 스냅샷."""

    dominant_constant: str
    resonance_score: float
    algebraic_closure: float
    boundary_alignment: float
    observer_alignment: float
    structural_health: float
    observations: List[IrrationalObservation] = field(default_factory=list)
    invariants: List[AlgebraicInvariant] = field(default_factory=list)
    metadata: Dict[str, float] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, object]:
        return {
            "dominant_constant": self.dominant_constant,
            "resonance_score": self.resonance_score,
            "algebraic_closure": self.algebraic_closure,
            "boundary_alignment": self.boundary_alignment,
            "observer_alignment": self.observer_alignment,
            "structural_health": self.structural_health,
            "observations": [obs.__dict__ for obs in self.observations],
            "invariants": [inv.__dict__ for inv in self.invariants],
            "metadata": dict(self.metadata),
        }
