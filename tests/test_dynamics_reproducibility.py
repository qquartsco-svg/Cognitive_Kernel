"""
재현성 축 테스트: time 의존 로직 mock, deterministic 테스트

테스트 범위:
- time 의존 로직 mock
- deterministic 테스트 (같은 입력 → 같은 출력)
- 시간 경과 시뮬레이션
"""

import pytest
import sys
import time
from unittest.mock import patch, MagicMock
from pathlib import Path

# 프로젝트 루트를 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from cognitive_kernel.engines.dynamics import DynamicsEngine, DynamicsConfig


class TestTimeMocking:
    """시간 의존 로직 mock 테스트"""
    
    def test_deterministic_entropy(self):
        """엔트로피 계산은 deterministic"""
        engine = DynamicsEngine()
        
        probs = [0.3, 0.4, 0.3]
        
        # 여러 번 계산
        entropy1 = engine.calculate_entropy(probs)
        entropy2 = engine.calculate_entropy(probs)
        entropy3 = engine.calculate_entropy(probs)
        
        # 모두 동일해야 함
        assert entropy1 == entropy2 == entropy3, \
            f"엔트로피 계산은 deterministic해야 함: {entropy1} == {entropy2} == {entropy3}"
    
    def test_deterministic_torque_same_phi(self):
        """같은 precession_phi에서 토크는 deterministic"""
        engine = DynamicsEngine()
        
        options = ["rest", "work", "exercise"]
        entropy = 0.8
        
        # precession_phi 고정
        engine.state.precession_phi = 0.5
        
        # 여러 번 계산
        torque1 = engine.generate_torque(options, entropy, mode="normal")
        engine.state.precession_phi = 0.5  # 다시 고정
        torque2 = engine.generate_torque(options, entropy, mode="normal")
        
        # 모두 동일해야 함
        assert torque1 == torque2, \
            f"같은 precession_phi에서 토크는 deterministic해야 함: {torque1} == {torque2}"
    
    @patch('time.time')
    def test_core_strength_time_mock(self, mock_time):
        """코어 강도 계산에 time mock 적용"""
        # 시간 고정
        fixed_time = 1000.0
        mock_time.return_value = fixed_time
        
        config = DynamicsConfig(core_decay_rate=0.01)
        engine = DynamicsEngine(config=config)
        
        memories = [
            {"importance": 0.9, "timestamp": fixed_time - 3600},
            {"importance": 0.8, "timestamp": fixed_time - 1800},
        ]
        
        # 첫 번째 계산
        core1 = engine.calculate_core_strength(memories)
        persistent1 = engine.state.persistent_core
        last_time1 = engine.state.last_decay_time
        
        # 시간 경과 (1초)
        mock_time.return_value = fixed_time + 1.0
        
        # 두 번째 계산
        core2 = engine.calculate_core_strength(memories)
        persistent2 = engine.state.persistent_core
        
        # persistent_core가 감쇠되었는지 확인
        if persistent1 is not None and persistent2 is not None:
            assert persistent2 < persistent1, \
                f"시간 경과에 persistent_core는 감소해야 함: {persistent1} -> {persistent2}"
    
    @patch('time.time')
    def test_memory_age_calculation(self, mock_time):
        """기억 나이 계산에 time mock 적용"""
        # 시간 고정
        fixed_time = 1000.0
        mock_time.return_value = fixed_time
        
        config = DynamicsConfig(
            old_memory_decay_rate=0.0001,
            new_memory_decay_rate=0.1,
            memory_age_threshold=3600.0,
        )
        engine = DynamicsEngine(config=config)
        
        # 오래된 기억 (임계값 초과)
        memories_old = [
            {"importance": 0.9, "timestamp": fixed_time - 7200},  # 2시간 전
        ]
        
        # 새 기억 (임계값 이하)
        memories_new = [
            {"importance": 0.9, "timestamp": fixed_time - 1800},  # 30분 전
        ]
        
        # 오래된 기억으로 코어 계산
        core_old = engine.calculate_core_strength(memories_old)
        
        # 새 기억으로 코어 계산
        engine.state.persistent_core = None  # 리셋
        engine.state.last_decay_time = None
        core_new = engine.calculate_core_strength(memories_new)
        
        # 코어 강도는 float이어야 함
        assert isinstance(core_old, float) and isinstance(core_new, float), \
            f"코어 강도는 float이어야 함: {type(core_old)}, {type(core_new)}"
    
    def test_reproducible_history(self):
        """히스토리는 재현 가능해야 함"""
        engine = DynamicsEngine()
        
        # 같은 엔트로피/코어로 여러 번 업데이트
        for i in range(5):
            engine.update_history(0.5, 0.5)
        
        history1 = engine.state.entropy_history.copy()
        history2 = engine.state.core_strength_history.copy()
        
        # 다시 업데이트
        engine.update_history(0.5, 0.5)
        
        # 이전 히스토리와 비교
        assert len(engine.state.entropy_history) == len(history1) + 1, \
            "히스토리는 순차적으로 추가되어야 함"
        assert engine.state.entropy_history[:-1] == history1, \
            "이전 히스토리는 유지되어야 함"


class TestDeterministicBehavior:
    """결정론적 동작 테스트"""
    
    def test_same_input_same_output(self):
        """같은 입력은 같은 출력"""
        engine1 = DynamicsEngine()
        engine2 = DynamicsEngine()
        
        probs = [0.3, 0.4, 0.3]
        
        entropy1 = engine1.calculate_entropy(probs)
        entropy2 = engine2.calculate_entropy(probs)
        
        assert entropy1 == entropy2, \
            f"같은 입력은 같은 출력이어야 함: {entropy1} == {entropy2}"
    
    def test_state_independence_deterministic(self):
        """상태 독립성은 deterministic"""
        engine1 = DynamicsEngine()
        engine2 = DynamicsEngine()
        
        # 같은 작업 수행
        probs = [0.3, 0.4, 0.3]
        entropy1 = engine1.calculate_entropy(probs)
        entropy2 = engine2.calculate_entropy(probs)
        
        # 같은 결과
        assert entropy1 == entropy2, \
            f"독립적인 엔진은 같은 결과를 가져야 함: {entropy1} == {entropy2}"
        
        # 같은 토크 생성
        options = ["rest", "work", "exercise"]
        engine1.state.precession_phi = 0.5
        engine2.state.precession_phi = 0.5
        
        torque1 = engine1.generate_torque(options, entropy1, mode="normal")
        torque2 = engine2.generate_torque(options, entropy2, mode="normal")
        
        assert torque1 == torque2, \
            f"같은 상태에서 같은 토크를 생성해야 함: {torque1} == {torque2}"
    
    def test_precession_phi_deterministic_update(self):
        """precession_phi 업데이트는 deterministic"""
        engine = DynamicsEngine()
        
        options = ["rest", "work", "exercise"]
        entropy = 0.8
        
        # 초기 phi
        initial_phi = engine.state.precession_phi
        
        # 토크 생성 (phi 업데이트됨)
        torque1 = engine.generate_torque(options, entropy, mode="normal")
        phi_after_1 = engine.state.precession_phi
        
        # 다시 토크 생성
        torque2 = engine.generate_torque(options, entropy, mode="normal")
        phi_after_2 = engine.state.precession_phi
        
        # phi는 omega만큼 증가해야 함
        omega = engine.config.omega
        expected_phi_1 = (initial_phi + omega) % (2 * 3.141592653589793)
        expected_phi_2 = (phi_after_1 + omega) % (2 * 3.141592653589793)
        
        assert abs(phi_after_1 - expected_phi_1) < 1e-6, \
            f"phi는 omega만큼 증가해야 함: {phi_after_1} ≈ {expected_phi_1}"
        assert abs(phi_after_2 - expected_phi_2) < 1e-6, \
            f"phi는 omega만큼 증가해야 함: {phi_after_2} ≈ {expected_phi_2}"

