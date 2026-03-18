"""
Boundary Refinement Loop - 경계 정제 루프

엔진 번호: 9번
엔진 이름: Boundary Convergence Engine
역할: 경계-공간 정합 계수로서의 π 개념 구현

Author: GNJz (Qquarts)
Version: 2.0.3
"""

import math
from typing import List, Optional
from .models import Point, ConvergenceState, ConvergenceResult
from .boundary_generator import BoundaryGenerator
from .density_estimator import InteriorDensityEstimator
from .mismatch_calculator import MismatchCalculator
from .convergence_controller import ConvergenceController
from .config import BoundaryConvergenceConfig


class BoundaryRefinementLoop:
    """경계 정제 루프
    
    경계를 반복적으로 정제하여 수렴시킵니다.
    """
    
    def __init__(self, config: BoundaryConvergenceConfig):
        """
        Args:
            config: 설정
        """
        self.config = config
        self.boundary_generator = BoundaryGenerator(config.boundary_radius)
        self.density_estimator = InteriorDensityEstimator(config.density_decay_factor)
        self.mismatch_calculator = MismatchCalculator()
        self.convergence_controller = ConvergenceController(
            error_threshold=config.error_threshold,
            max_iterations=config.max_iterations,
            convergence_rate_threshold=config.convergence_rate_threshold
        )
    
    def refine(self, importance_weights: Optional[dict] = None) -> ConvergenceResult:
        """경계 정제
        
        경계를 반복적으로 정제하여 수렴시킵니다.
        
        Args:
            importance_weights: 중요도 가중치 (선택)
            
        Returns:
            수렴 결과
        """
        result = ConvergenceResult(
            iteration=0,
            boundary_points=0,
            perimeter_estimate=0.0,
            area_estimate=0.0,
            mismatch=float('inf'),
            convergence_rate=0.0,
            converged=False
        )
        
        # 초기 경계 생성
        boundary = self.boundary_generator.generate_initial_boundary(
            self.config.initial_boundary_points
        )
        
        previous_mismatch = float('inf')
        iteration = 0
        
        while iteration < self.config.max_iterations:
            # 경계 길이 계산
            perimeter = self.boundary_generator.calculate_perimeter(boundary)
            
            # 면적 계산
            area = self.mismatch_calculator.calculate_area(boundary)
            
            # 불일치 계산
            mismatch = self.mismatch_calculator.calculate_mismatch(
                perimeter=perimeter,
                area=area,
                radius=self.config.boundary_radius
            )
            
            # 수렴률 계산
            convergence_rate = self.mismatch_calculator.calculate_convergence_rate(
                current_mismatch=mismatch,
                previous_mismatch=previous_mismatch
            )
            
            # 내부 점 생성
            interior_points = self.density_estimator.generate_interior_points(
                boundary=boundary,
                density=self.config.interior_point_density
            )
            
            # 밀도 추정
            density = self.density_estimator.estimate_density(
                boundary=boundary,
                interior_points=interior_points,
                importance_weights=importance_weights
            )
            
            # 밀도 맵 생성 (첫 반복 또는 주기적으로)
            if iteration == 0 or iteration % 10 == 0:
                density_map = self.density_estimator.create_density_map(
                    boundary=boundary,
                    interior_points=interior_points,
                    resolution=self.config.density_resolution
                )
                result.density_map.update(density_map)
            
            # 상태 저장
            state = ConvergenceState(
                iteration=iteration,
                boundary_points=len(boundary),
                perimeter_estimate=perimeter,
                area_estimate=area,
                mismatch=mismatch,
                convergence_rate=convergence_rate,
                density=density
            )
            result.add_state(state)
            
            # 결과 업데이트
            result.iteration = iteration
            result.boundary_points = len(boundary)
            result.perimeter_estimate = perimeter
            result.area_estimate = area
            result.mismatch = mismatch
            result.convergence_rate = convergence_rate
            
            # 수렴 확인
            if self.convergence_controller.check_convergence(
                mismatch=mismatch,
                iteration=iteration,
                convergence_rate=convergence_rate
            ):
                result.converged = True
                break
            
            # 경계 정제
            # 옵션 1: 재샘플링 (점 개수 증가)
            if iteration % 3 == 0:
                boundary = self.boundary_generator.refine_boundary(
                    boundary=boundary,
                    refinement_factor=self.config.refinement_factor
                )
            else:
                # 옵션 2: 밀도 기울기 반영 (공간이 원을 만들도록 압박)
                if self.config.use_density_gradient and result.density_map:
                    boundary = self.boundary_generator.refine_boundary_with_density_gradient(
                        boundary=boundary,
                        density_map=result.density_map,
                        learning_rate=self.config.force_learning_rate
                    )
                
                # 옵션 3: mismatch 힘 반영 (경계-공간 정합)
                if self.config.use_mismatch_force:
                    mismatch_forces = self.mismatch_calculator.calculate_mismatch_force(
                        boundary=boundary,
                        perimeter=perimeter,
                        area=area,
                        radius=self.config.boundary_radius
                    )
                    
                    # 힘을 경계에 적용
                    new_boundary = []
                    for i, point in enumerate(boundary):
                        fx, fy = mismatch_forces[i]
                        new_x = point.x + fx * self.config.force_learning_rate
                        new_y = point.y + fy * self.config.force_learning_rate
                        # 반지름 제약
                        distance = math.sqrt(new_x**2 + new_y**2)
                        if distance > 0:
                            scale = self.config.boundary_radius / distance
                            new_x *= scale
                            new_y *= scale
                        new_boundary.append(Point(new_x, new_y))
                    boundary = new_boundary
            
            previous_mismatch = mismatch
            iteration += 1
        
        return result

