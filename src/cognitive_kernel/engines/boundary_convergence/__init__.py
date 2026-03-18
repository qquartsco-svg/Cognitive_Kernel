"""
Boundary Convergence Engine Package

엔진 번호: 9번
엔진 이름: Boundary Convergence Engine
역할: 경계-공간 정합 계수로서의 π 개념 구현

⚠️ 중요 명확화:
- 이 엔진은 π를 계산하는 것이 아니라,
- 경계-공간 정합의 동역학적 과정을 구현합니다.
- 출력은 π 값이 아니라 수렴 과정입니다.

핵심 개념:
- 경계(선)가 생기면 → 내부 공간이 생기고
- 내부를 채우기 위해 경계가 끝없이 보정되는 과정
- π는 결과가 아니라 과정이다

주요 기능:
- Boundary Generator: 경계 생성
- Interior Density Estimator: 내부 밀도 추정
- Mismatch Calculator: 불일치 계산
- Boundary Refinement Loop: 경계 정제 루프
- Convergence Controller: 수렴 제어

Author: GNJz (Qquarts)
Version: 2.0.3
"""

from .boundary_convergence_engine import BoundaryConvergenceEngine
from .config import BoundaryConvergenceConfig
from .models import ConvergenceResult, ConvergenceState, Point

__all__ = [
    "BoundaryConvergenceEngine",
    "BoundaryConvergenceConfig",
    "ConvergenceResult",
    "ConvergenceState",
    "Point",
]

__version__ = "1.0.0"

