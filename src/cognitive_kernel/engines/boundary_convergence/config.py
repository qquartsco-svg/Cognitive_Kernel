"""
Boundary Convergence Engine Configuration

엔진 번호: 9번
엔진 이름: Boundary Convergence Engine
역할: 경계-공간 정합 계수로서의 π 개념 구현

Author: GNJz (Qquarts)
Version: 2.0.3
"""

from dataclasses import dataclass


@dataclass
class BoundaryConvergenceConfig:
    """Boundary Convergence Engine 설정"""
    
    # 경계 생성 파라미터
    initial_boundary_points: int = 4  # 초기 경계 점 개수 (최소 3)
    boundary_radius: float = 1.0  # 경계 반지름
    
    # 밀도 추정 파라미터
    density_resolution: int = 100  # 밀도 계산 해상도
    density_decay_factor: float = 0.1  # 밀도 감쇠 계수
    
    # 수렴 제어 파라미터
    error_threshold: float = 1e-6  # 임계 오차
    max_iterations: int = 1000  # 최대 반복 횟수
    convergence_rate_threshold: float = 1e-9  # 수렴률 임계값
    
    # 경계 정제 파라미터
    refinement_factor: float = 2.0  # 경계 점 증가 배수 (N *= refinement_factor)
    curvature_smoothing: float = 0.5  # 곡률 평활화 계수
    
    # 내부 점 생성 파라미터
    interior_point_density: float = 0.1  # 내부 점 밀도 (점/단위면적)
    
    # 경계 정제 모드
    use_density_gradient: bool = True  # 밀도 기울기 반영 여부
    use_mismatch_force: bool = True  # mismatch 힘 반영 여부
    force_learning_rate: float = 0.01  # 힘 적용 학습률
    
    def __post_init__(self):
        """설정 검증"""
        if self.initial_boundary_points < 3:
            raise ValueError("initial_boundary_points는 최소 3이어야 합니다")
        if self.boundary_radius <= 0:
            raise ValueError("boundary_radius는 양수여야 합니다")
        if self.error_threshold <= 0:
            raise ValueError("error_threshold는 양수여야 합니다")
        if self.max_iterations <= 0:
            raise ValueError("max_iterations는 양수여야 합니다")

