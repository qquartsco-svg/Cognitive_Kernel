"""
Mismatch Calculator - 불일치 계산기

엔진 번호: 9번
엔진 이름: Boundary Convergence Engine
역할: 경계-공간 정합 계수로서의 π 개념 구현

Author: GNJz (Qquarts)
Version: 2.0.3
"""

import math
from typing import List
from .models import Point


class MismatchCalculator:
    """불일치 계산기
    
    경계 길이와 내부 면적 간의 불일치를 계산합니다.
    이 불일치가 수렴의 목표입니다.
    """
    
    def calculate_mismatch(self, perimeter: float, area: float, radius: float) -> float:
        """불일치 계산
        
        경계 길이와 면적의 이론값과 추정값 간의 불일치를 계산합니다.
        
        Args:
            perimeter: 경계 길이 추정값
            area: 면적 추정값
            radius: 반지름
            
        Returns:
            불일치 오차
        """
        # 이론값
        theoretical_perimeter = 2 * math.pi * radius
        theoretical_area = math.pi * radius**2
        
        # 오차 계산
        perimeter_error = abs(perimeter - theoretical_perimeter) / theoretical_perimeter
        area_error = abs(area - theoretical_area) / theoretical_area
        
        # 전체 불일치 (가중 평균)
        mismatch = (perimeter_error + area_error) / 2.0
        
        return mismatch
    
    def calculate_area(self, boundary: List[Point]) -> float:
        """면적 계산 (Shoelace 공식)
        
        다각형의 면적을 계산합니다.
        
        Args:
            boundary: 경계 점 리스트
            
        Returns:
            면적
        """
        if len(boundary) < 3:
            return 0.0
        
        area = 0.0
        n = len(boundary)
        
        for i in range(n):
            j = (i + 1) % n
            area += boundary[i].x * boundary[j].y
            area -= boundary[j].x * boundary[i].y
        
        return abs(area) / 2.0
    
    def calculate_convergence_rate(self, current_mismatch: float, 
                                  previous_mismatch: float) -> float:
        """수렴률 계산
        
        이전 반복과 현재 반복의 불일치 변화율을 계산합니다.
        
        Args:
            current_mismatch: 현재 불일치
            previous_mismatch: 이전 불일치
            
        Returns:
            수렴률 (음수면 수렴, 양수면 발산)
        """
        if previous_mismatch == 0:
            return 0.0
        
        rate = (current_mismatch - previous_mismatch) / previous_mismatch
        return rate
    
    def calculate_mismatch_force(self, boundary: List[Point], 
                                perimeter: float, area: float, 
                                radius: float) -> List[tuple]:
        """불일치 힘 계산
        
        mismatch를 종료 조건이 아니라 경계를 변형시키는 힘으로 사용합니다.
        
        Args:
            boundary: 경계 점 리스트
            perimeter: 현재 경계 길이
            area: 현재 면적
            radius: 목표 반지름
            
        Returns:
            각 경계 점에 대한 힘 벡터 리스트 [(fx, fy), ...]
        """
        # 이론값
        theoretical_perimeter = 2 * math.pi * radius
        theoretical_area = math.pi * radius**2
        
        # 오차
        perimeter_error = (perimeter - theoretical_perimeter) / theoretical_perimeter
        area_error = (area - theoretical_area) / theoretical_area
        
        # 힘 계산: 오차를 줄이는 방향
        forces = []
        
        for i, point in enumerate(boundary):
            # 중심까지의 거리
            distance = math.sqrt(point.x**2 + point.y**2)
            
            # 반지름 오차
            radius_error = (distance - radius) / radius
            
            # 힘 방향: 중심 방향 (반지름 오차를 줄이기 위해)
            if distance > 0:
                fx = -(point.x / distance) * radius_error
                fy = -(point.y / distance) * radius_error
            else:
                fx = 0.0
                fy = 0.0
            
            # 면적 오차 반영 (면적이 작으면 밖으로, 크면 안으로)
            if area < theoretical_area:
                # 면적이 작으면 밖으로 밀기
                fx += (point.x / distance) * abs(area_error) if distance > 0 else 0.0
                fy += (point.y / distance) * abs(area_error) if distance > 0 else 0.0
            else:
                # 면적이 크면 안으로 당기기
                fx -= (point.x / distance) * abs(area_error) if distance > 0 else 0.0
                fy -= (point.y / distance) * abs(area_error) if distance > 0 else 0.0
            
            forces.append((fx, fy))
        
        return forces

