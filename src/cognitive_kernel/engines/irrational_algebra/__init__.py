"""
Irrational Algebra Engine Package

무리수와 대수적 불변식을 물리-동역학 관점에서 해석하는 기초 엔진.

핵심 역할:
- pi, sqrt(2), phi, e 같은 무리수 상수군을 구조적 비율로 해석
- 상태 벡터의 비율이 어떤 무리수 공명에 가까운지 측정
- 대수적 불변식(예: phi^2 - phi - 1 = 0) 잔차를 계산
- boundary_convergence, observer 건강도와 연결 가능한 스냅샷 생성
"""

from .config import IrrationalAlgebraConfig
from .models import (
    IrrationalConstant,
    IrrationalObservation,
    AlgebraicInvariant,
    IrrationalAlgebraSnapshot,
)
from .irrational_algebra_engine import IrrationalAlgebraEngine

__all__ = [
    "IrrationalAlgebraConfig",
    "IrrationalConstant",
    "IrrationalObservation",
    "AlgebraicInvariant",
    "IrrationalAlgebraSnapshot",
    "IrrationalAlgebraEngine",
]

__version__ = "1.0.0"
