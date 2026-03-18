"""
Boundary Convergence Engine - Data Models

엔진 번호: 9번
엔진 이름: Boundary Convergence Engine
역할: 경계-공간 정합 계수로서의 π 개념 구현

Author: GNJz (Qquarts)
Version: 2.0.3
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import math


@dataclass
class Point:
    """2D 점 좌표"""
    x: float
    y: float
    
    def distance_to(self, other: 'Point') -> float:
        """다른 점까지의 거리"""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return False
        return abs(self.x - other.x) < 1e-9 and abs(self.y - other.y) < 1e-9


@dataclass
class ConvergenceState:
    """수렴 상태"""
    iteration: int
    boundary_points: int
    perimeter_estimate: float
    area_estimate: float
    mismatch: float
    convergence_rate: float
    density: float


@dataclass
class ConvergenceResult:
    """수렴 과정 결과
    
    ⚠️ 중요: 이 엔진은 π를 계산하는 것이 아니라,
    경계-공간 정합의 동역학적 과정을 구현합니다.
    
    출력은 π 값이 아니라 수렴 과정입니다.
    """
    iteration: int  # 반복 횟수
    boundary_points: int  # 경계 점 개수
    perimeter_estimate: float  # 경계 길이 추정값
    area_estimate: float  # 면적 추정값
    mismatch: float  # 불일치 오차
    convergence_rate: float  # 수렴률
    density_map: Dict[Point, float] = field(default_factory=dict)  # 밀도 맵
    history: List[ConvergenceState] = field(default_factory=list)  # 수렴 히스토리
    converged: bool = False  # 수렴 완료 여부
    
    def add_state(self, state: ConvergenceState) -> None:
        """상태 추가"""
        self.history.append(state)
    
    def get_latest_state(self) -> Optional[ConvergenceState]:
        """최신 상태 반환"""
        return self.history[-1] if self.history else None

