"""
Convergence Controller - 수렴 제어기

엔진 번호: 9번
엔진 이름: Boundary Convergence Engine
역할: 경계-공간 정합 계수로서의 π 개념 구현

Author: GNJz (Qquarts)
Version: 2.0.3
"""

from typing import Optional
from .models import ConvergenceState


class ConvergenceController:
    """수렴 제어기
    
    수렴 과정을 제어하고 수렴 완료 여부를 판단합니다.
    """
    
    def __init__(self, error_threshold: float = 1e-6,
                 max_iterations: int = 1000,
                 convergence_rate_threshold: float = 1e-9):
        """
        Args:
            error_threshold: 임계 오차
            max_iterations: 최대 반복 횟수
            convergence_rate_threshold: 수렴률 임계값
        """
        self.error_threshold = error_threshold
        self.max_iterations = max_iterations
        self.convergence_rate_threshold = convergence_rate_threshold
    
    def check_convergence(self, mismatch: float, 
                         iteration: int,
                         convergence_rate: float) -> bool:
        """수렴 확인
        
        수렴 완료 여부를 판단합니다.
        
        Args:
            mismatch: 현재 불일치
            iteration: 현재 반복 횟수
            convergence_rate: 수렴률
            
        Returns:
            수렴 완료 여부
        """
        # 최대 반복 횟수 초과
        if iteration >= self.max_iterations:
            return True
        
        # 오차 임계값 이하
        if mismatch < self.error_threshold:
            return True
        
        # 수렴률 임계값 이하 (거의 변화 없음)
        if abs(convergence_rate) < self.convergence_rate_threshold:
            return True
        
        return False
    
    def should_continue(self, state: Optional[ConvergenceState]) -> bool:
        """계속 진행 여부 확인
        
        Args:
            state: 현재 수렴 상태
            
        Returns:
            계속 진행 여부
        """
        if state is None:
            return True
        
        return not self.check_convergence(
            mismatch=state.mismatch,
            iteration=state.iteration,
            convergence_rate=state.convergence_rate
        )

