"""
Boundary Generator - 경계 생성기

엔진 번호: 9번
엔진 이름: Boundary Convergence Engine
역할: 경계-공간 정합 계수로서의 π 개념 구현

Author: GNJz (Qquarts)
Version: 2.0.3
"""

import math
from typing import List
from .models import Point


class BoundaryGenerator:
    """경계 생성기
    
    초기 원형 경계를 생성합니다.
    경계는 거친 다각형으로 시작하여 정제 과정을 거칩니다.
    """
    
    def __init__(self, radius: float = 1.0):
        """
        Args:
            radius: 경계 반지름
        """
        self.radius = radius
    
    def generate_initial_boundary(self, n_points: int) -> List[Point]:
        """초기 경계 생성
        
        원형 경계를 n_points개의 점으로 근사합니다.
        
        Args:
            n_points: 경계 점 개수 (최소 3)
            
        Returns:
            경계 점 리스트
        """
        if n_points < 3:
            raise ValueError("n_points는 최소 3이어야 합니다")
        
        boundary = []
        for i in range(n_points):
            # 균등하게 분포된 각도
            angle = 2 * math.pi * i / n_points
            x = self.radius * math.cos(angle)
            y = self.radius * math.sin(angle)
            boundary.append(Point(x, y))
        
        return boundary
    
    def refine_boundary(self, boundary: List[Point], refinement_factor: float = 2.0) -> List[Point]:
        """경계 정제 (재샘플링)
        
        기존 경계 점 사이에 새로운 점을 추가하여 경계를 정제합니다.
        현재는 재샘플링만 수행합니다.
        
        Args:
            boundary: 기존 경계 점 리스트
            refinement_factor: 점 개수 증가 배수
            
        Returns:
            정제된 경계 점 리스트
        """
        if len(boundary) < 2:
            return boundary
        
        refined = []
        n = len(boundary)
        new_n = int(n * refinement_factor)
        
        for i in range(new_n):
            # 기존 점 사이의 보간
            angle = 2 * math.pi * i / new_n
            x = self.radius * math.cos(angle)
            y = self.radius * math.sin(angle)
            refined.append(Point(x, y))
        
        return refined
    
    def refine_boundary_with_density_gradient(self, boundary: List[Point],
                                             density_map: dict,
                                             learning_rate: float = 0.01) -> List[Point]:
        """경계 정제 (밀도 기울기 반영)
        
        밀도 맵의 기울기를 반영하여 경계를 실제로 정제합니다.
        공간이 원을 만들도록 압박하는 과정을 구현합니다.
        
        Args:
            boundary: 기존 경계 점 리스트
            density_map: 밀도 맵 (Point -> density)
            learning_rate: 학습률 (경계 이동 속도)
            
        Returns:
            정제된 경계 점 리스트
        """
        if len(boundary) < 2 or not density_map:
            return boundary
        
        refined = []
        
        for point in boundary:
            # 경계 점의 법선 벡터 추정
            normal = self._estimate_normal(boundary, point)
            
            # 밀도 기울기 계산
            density_gradient = self._calculate_density_gradient(point, density_map)
            
            # 압력 계산: 밀도 기울기와 법선의 내적
            pressure = density_gradient[0] * normal[0] + density_gradient[1] * normal[1]
            
            # 경계 이동: 압력에 비례하여 법선 방향으로 이동
            new_x = point.x + normal[0] * pressure * learning_rate
            new_y = point.y + normal[1] * pressure * learning_rate
            
            # 반지름 제약 (너무 멀어지지 않도록)
            distance = math.sqrt(new_x**2 + new_y**2)
            if distance > 0:
                scale = self.radius / distance
                new_x *= scale
                new_y *= scale
            
            refined.append(Point(new_x, new_y))
        
        return refined
    
    def _estimate_normal(self, boundary: List[Point], point: Point) -> tuple:
        """법선 벡터 추정
        
        경계 점에서의 법선 벡터를 추정합니다.
        
        Args:
            boundary: 경계 점 리스트
            point: 현재 점
            
        Returns:
            (nx, ny) 법선 벡터
        """
        # 현재 점의 인덱스 찾기
        try:
            idx = boundary.index(point)
        except ValueError:
            # 점을 찾을 수 없으면 중심 방향
            return (point.x / self.radius, point.y / self.radius)
        
        # 이전 점과 다음 점
        prev_idx = (idx - 1) % len(boundary)
        next_idx = (idx + 1) % len(boundary)
        
        prev_point = boundary[prev_idx]
        next_point = boundary[next_idx]
        
        # 접선 벡터
        tangent_x = next_point.x - prev_point.x
        tangent_y = next_point.y - prev_point.y
        
        # 법선 벡터 (접선에 수직)
        normal_x = -tangent_y
        normal_y = tangent_x
        
        # 정규화
        norm = math.sqrt(normal_x**2 + normal_y**2)
        if norm > 0:
            normal_x /= norm
            normal_y /= norm
        
        return (normal_x, normal_y)
    
    def _calculate_density_gradient(self, point: Point, density_map: dict) -> tuple:
        """밀도 기울기 계산
        
        점 주변의 밀도 기울기를 계산합니다.
        
        Args:
            point: 현재 점
            density_map: 밀도 맵
            
        Returns:
            (gx, gy) 밀도 기울기
        """
        if not density_map:
            return (0.0, 0.0)
        
        # 주변 점들의 밀도 샘플링
        sample_radius = 0.1
        samples = []
        
        for map_point, density in density_map.items():
            distance = point.distance_to(map_point)
            if distance < sample_radius:
                samples.append((map_point, density, distance))
        
        if len(samples) < 2:
            return (0.0, 0.0)
        
        # 기울기 계산 (중앙 차분)
        gx = 0.0
        gy = 0.0
        
        for map_point, density, dist in samples:
            if dist > 0:
                dx = (map_point.x - point.x) / dist
                dy = (map_point.y - point.y) / dist
                weight = 1.0 / (dist + 1e-6)
                gx += dx * density * weight
                gy += dy * density * weight
        
        # 정규화
        total_weight = sum(1.0 / (dist + 1e-6) for _, _, dist in samples)
        if total_weight > 0:
            gx /= total_weight
            gy /= total_weight
        
        return (gx, gy)
    
    def calculate_perimeter(self, boundary: List[Point]) -> float:
        """경계 길이 계산
        
        다각형의 둘레를 계산합니다.
        
        Args:
            boundary: 경계 점 리스트
            
        Returns:
            경계 길이
        """
        if len(boundary) < 3:
            return 0.0
        
        perimeter = 0.0
        for i in range(len(boundary)):
            p1 = boundary[i]
            p2 = boundary[(i + 1) % len(boundary)]
            perimeter += p1.distance_to(p2)
        
        return perimeter

