"""
Interior Density Estimator - 내부 밀도 추정기

엔진 번호: 9번
엔진 이름: Boundary Convergence Engine
역할: 경계-공간 정합 계수로서의 π 개념 구현

Author: GNJz (Qquarts)
Version: 2.0.3
"""

import math
from typing import List, Dict, Optional
from .models import Point


class InteriorDensityEstimator:
    """내부 밀도 추정기
    
    경계 내부 공간의 밀도를 추정합니다.
    공간을 채우는 과정을 수치화합니다.
    """
    
    def __init__(self, decay_factor: float = 0.1):
        """
        Args:
            decay_factor: 밀도 감쇠 계수 (거리에 따른 감쇠)
        """
        self.decay_factor = decay_factor
    
    def generate_interior_points(self, boundary: List[Point], density: float = 0.1) -> List[Point]:
        """내부 점 생성
        
        경계 내부에 균등하게 분포된 점을 생성합니다.
        
        Args:
            boundary: 경계 점 리스트
            density: 점 밀도 (점/단위면적)
            
        Returns:
            내부 점 리스트
        """
        if len(boundary) < 3:
            return []
        
        # 경계의 중심 계산
        center_x = sum(p.x for p in boundary) / len(boundary)
        center_y = sum(p.y for p in boundary) / len(boundary)
        center = Point(center_x, center_y)
        
        # 경계의 최대 반지름 추정
        max_radius = max(center.distance_to(p) for p in boundary)
        
        # 내부 점 생성 (격자 패턴)
        interior_points = []
        grid_size = int(math.sqrt(density * math.pi * max_radius**2))
        
        for i in range(-grid_size, grid_size + 1):
            for j in range(-grid_size, grid_size + 1):
                x = center.x + (i / grid_size) * max_radius * 0.9
                y = center.y + (j / grid_size) * max_radius * 0.9
                point = Point(x, y)
                
                # 경계 내부인지 확인 (간단한 원형 체크)
                if center.distance_to(point) < max_radius * 0.9:
                    interior_points.append(point)
        
        return interior_points
    
    def estimate_density(self, boundary: List[Point], 
                        interior_points: List[Point],
                        importance_weights: Optional[Dict[Point, float]] = None) -> float:
        """밀도 추정
        
        경계 내부의 밀도를 추정합니다.
        
        Args:
            boundary: 경계 점 리스트
            interior_points: 내부 점 리스트
            importance_weights: 중요도 가중치 (선택)
            
        Returns:
            평균 밀도
        """
        if not interior_points:
            return 0.0
        
        # 경계의 중심 계산
        center_x = sum(p.x for p in boundary) / len(boundary)
        center_y = sum(p.y for p in boundary) / len(boundary)
        center = Point(center_x, center_y)
        
        # 경계의 최대 반지름 추정
        max_radius = max(center.distance_to(p) for p in boundary)
        
        # 면적 추정
        estimated_area = math.pi * max_radius**2
        
        # 밀도 계산
        if importance_weights:
            # 가중치가 있는 경우
            total_weight = sum(
                importance_weights.get(point, 1.0) 
                for point in interior_points
            )
            density = total_weight / estimated_area if estimated_area > 0 else 0.0
        else:
            # 가중치가 없는 경우
            density = len(interior_points) / estimated_area if estimated_area > 0 else 0.0
        
        return density
    
    def create_density_map(self, boundary: List[Point],
                          interior_points: List[Point],
                          resolution: int = 100) -> Dict[Point, float]:
        """밀도 맵 생성
        
        경계 내부의 밀도를 공간적으로 매핑합니다.
        
        Args:
            boundary: 경계 점 리스트
            interior_points: 내부 점 리스트
            resolution: 해상도
            
        Returns:
            밀도 맵 (Point -> density)
        """
        if not interior_points:
            return {}
        
        # 경계의 중심 계산
        center_x = sum(p.x for p in boundary) / len(boundary)
        center_y = sum(p.y for p in boundary) / len(boundary)
        center = Point(center_x, center_y)
        
        # 경계의 최대 반지름 추정
        max_radius = max(center.distance_to(p) for p in boundary)
        
        density_map = {}
        
        # 격자 패턴으로 밀도 계산
        for i in range(resolution):
            for j in range(resolution):
                x = center.x + (i / resolution - 0.5) * max_radius * 2
                y = center.y + (j / resolution - 0.5) * max_radius * 2
                point = Point(x, y)
                
                # 경계 내부인지 확인
                if center.distance_to(point) < max_radius * 0.9:
                    # 주변 점들의 밀도 계산
                    density = 0.0
                    for interior_point in interior_points:
                        distance = point.distance_to(interior_point)
                        if distance < max_radius * 0.1:
                            density += math.exp(-self.decay_factor * distance)
                    
                    density_map[point] = density
        
        return density_map

