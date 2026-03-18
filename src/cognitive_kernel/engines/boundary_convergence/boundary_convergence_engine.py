"""
Boundary Convergence Engine - 메인 엔진

엔진 번호: 9번
엔진 이름: Boundary Convergence Engine
역할: 경계-공간 정합 계수로서의 π 개념 구현

⚠️ 중요 명확화:
- 이 엔진은 π를 계산하는 것이 아니라,
- 경계-공간 정합의 동역학적 과정을 구현합니다.
- 출력은 π 값이 아니라 수렴 과정입니다.

Author: GNJz (Qquarts)
Version: 2.0.3
"""

from typing import Optional, Dict
from .config import BoundaryConvergenceConfig
from .refinement_loop import BoundaryRefinementLoop
from .models import ConvergenceResult, Point


class BoundaryConvergenceEngine:
    """Boundary Convergence Engine
    
    경계-공간 정합 계수로서의 π 개념을 구현하는 엔진.
    
    핵심 개념:
    - 경계(선)가 생기면 → 내부 공간이 생기고
    - 내부를 채우기 위해 경계가 끝없이 보정되는 과정
    - π는 결과가 아니라 과정이다
    """
    
    def __init__(self, config: Optional[BoundaryConvergenceConfig] = None):
        """
        Args:
            config: 설정 (None이면 기본값 사용)
        """
        self.config = config or BoundaryConvergenceConfig()
        self.refinement_loop = BoundaryRefinementLoop(self.config)
    
    def converge(self, importance_weights: Optional[Dict[Point, float]] = None) -> ConvergenceResult:
        """수렴 실행
        
        경계-공간 정합 과정을 실행합니다.
        
        Args:
            importance_weights: 중요도 가중치 (선택)
                - 기억의 중요도를 밀도로 변환할 때 사용
                - None이면 균등 밀도 사용
        
        Returns:
            수렴 결과 (π 값이 아니라 수렴 과정)
        """
        return self.refinement_loop.refine(importance_weights=importance_weights)
    
    def reset(self) -> None:
        """엔진 리셋"""
        self.refinement_loop = BoundaryRefinementLoop(self.config)
    
    def get_config(self) -> BoundaryConvergenceConfig:
        """설정 반환"""
        return self.config
    
    def update_config(self, **kwargs) -> None:
        """설정 업데이트
        
        Args:
            **kwargs: 업데이트할 설정 파라미터
        """
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        
        # 설정 변경 후 리셋
        self.reset()

