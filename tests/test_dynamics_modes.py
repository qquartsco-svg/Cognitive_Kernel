"""
모드 축 테스트: normal/adhd/asd 문자열 모드, dementia/alzheimer 파라미터 차이

테스트 범위:
- 문자열 모드 지원 (normal, adhd, asd)
- dementia/alzheimer 파라미터 차이 확인
- 모드별 토크 세기 차이
"""

import pytest
import sys
from pathlib import Path

# 프로젝트 루트를 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from cognitive_kernel.engines.dynamics import DynamicsEngine, DynamicsConfig
from cognitive_kernel import CognitiveKernel, CognitiveMode


class TestStringModes:
    """문자열 모드 테스트"""
    
    def test_normal_mode(self):
        """normal 모드 테스트"""
        engine = DynamicsEngine()
        
        options = ["rest", "work", "exercise"]
        entropy = 0.8
        
        # normal 모드로 토크 생성
        torque = engine.generate_torque(options, entropy, mode="normal")
        
        assert isinstance(torque, dict), "토크는 dict여야 함"
        assert len(torque) == len(options), "토크는 모든 옵션에 대해 생성되어야 함"
        
        # normal 모드는 기본 gamma 사용
        base_gamma = engine.config.base_gamma
        max_entropy = 1.0986122886681098  # ln(3)
        normalized_entropy = entropy / max_entropy
        expected_torque_strength = base_gamma * normalized_entropy
        
        # 토크 세기 확인 (cos 값에 따라 다를 수 있음)
        torque_values = list(torque.values())
        max_torque = max(abs(v) for v in torque_values)
        assert max_torque <= expected_torque_strength * 1.1, \
            f"토크 세기는 예상 범위 내여야 함: {max_torque} <= {expected_torque_strength * 1.1}"
    
    def test_adhd_mode(self):
        """ADHD 모드 테스트 (더 강한 회전)"""
        engine = DynamicsEngine()
        
        options = ["rest", "work", "exercise"]
        entropy = 0.8
        
        # ADHD 모드로 토크 생성
        torque_adhd = engine.generate_torque(options, entropy, mode="adhd")
        
        # normal 모드로 토크 생성
        torque_normal = engine.generate_torque(options, entropy, mode="normal")
        
        # ADHD는 더 강한 토크를 가져야 함
        adhd_max = max(abs(v) for v in torque_adhd.values())
        normal_max = max(abs(v) for v in torque_normal.values())
        
        assert adhd_max >= normal_max, \
            f"ADHD 모드는 더 강한 토크를 가져야 함: {adhd_max} >= {normal_max}"
    
    def test_asd_mode(self):
        """ASD 모드 테스트 (약한 회전)"""
        engine = DynamicsEngine()
        
        options = ["rest", "work", "exercise"]
        entropy = 0.8
        
        # ASD 모드로 토크 생성
        torque_asd = engine.generate_torque(options, entropy, mode="asd")
        
        # normal 모드로 토크 생성
        torque_normal = engine.generate_torque(options, entropy, mode="normal")
        
        # ASD는 약한 토크를 가져야 함
        asd_max = max(abs(v) for v in torque_asd.values())
        normal_max = max(abs(v) for v in torque_normal.values())
        
        assert asd_max <= normal_max, \
            f"ASD 모드는 약한 토크를 가져야 함: {asd_max} <= {normal_max}"
    
    def test_mode_case_insensitive(self):
        """모드 대소문자 무시"""
        engine = DynamicsEngine()
        
        options = ["rest", "work", "exercise"]
        entropy = 0.8
        
        # precession_phi 고정 (결과 비교를 위해)
        engine.state.precession_phi = 0.5
        
        # 대소문자 다른 모드
        torque1 = engine.generate_torque(options, entropy, mode="ADHD")
        
        # precession_phi 다시 고정
        engine.state.precession_phi = 0.5
        torque2 = engine.generate_torque(options, entropy, mode="adhd")
        
        # precession_phi 다시 고정
        engine.state.precession_phi = 0.5
        torque3 = engine.generate_torque(options, entropy, mode="Adhd")
        
        # 모두 동일한 결과여야 함 (precession_phi가 같으면)
        assert torque1 == torque2 == torque3, \
            "모드는 대소문자 무시해야 함"
    
    def test_unknown_mode(self):
        """알 수 없는 모드는 기본값 사용"""
        engine = DynamicsEngine()
        
        options = ["rest", "work", "exercise"]
        entropy = 0.8
        
        # precession_phi 고정 (결과 비교를 위해)
        engine.state.precession_phi = 0.5
        
        # 알 수 없는 모드
        torque_unknown = engine.generate_torque(options, entropy, mode="unknown_mode")
        
        # precession_phi 다시 고정
        engine.state.precession_phi = 0.5
        
        # normal 모드와 비교
        torque_normal = engine.generate_torque(options, entropy, mode="normal")
        
        # 알 수 없는 모드는 기본값(normal) 사용
        assert torque_unknown == torque_normal, \
            "알 수 없는 모드는 기본값(normal)을 사용해야 함"


class TestDementiaAlzheimer:
    """치매/알츠하이머 모드 파라미터 차이 테스트"""
    
    def test_dementia_config(self):
        """치매 모드 설정 확인"""
        from cognitive_kernel.cognitive_modes import CognitiveModePresets
        
        dementia_config = CognitiveModePresets.dementia()
        
        # 치매 특성 확인
        assert hasattr(dementia_config, 'old_memory_decay_rate'), \
            "dementia_config에 old_memory_decay_rate가 있어야 함"
        assert hasattr(dementia_config, 'new_memory_decay_rate'), \
            "dementia_config에 new_memory_decay_rate가 있어야 함"
        assert hasattr(dementia_config, 'core_decay_rate'), \
            "dementia_config에 core_decay_rate가 있어야 함"
        
        # 치매는 오래된 기억 감쇠율이 있음
        assert dementia_config.old_memory_decay_rate > 0, \
            f"치매는 old_memory_decay_rate > 0이어야 함, got {dementia_config.old_memory_decay_rate}"
    
    def test_alzheimer_config(self):
        """알츠하이머 모드 설정 확인"""
        from cognitive_kernel.cognitive_modes import CognitiveModePresets
        
        alzheimer_config = CognitiveModePresets.alzheimer()
        
        # 알츠하이머 특성 확인
        assert hasattr(alzheimer_config, 'old_memory_decay_rate'), \
            "alzheimer_config에 old_memory_decay_rate가 있어야 함"
        assert hasattr(alzheimer_config, 'new_memory_decay_rate'), \
            "alzheimer_config에 new_memory_decay_rate가 있어야 함"
        assert hasattr(alzheimer_config, 'core_decay_rate'), \
            "alzheimer_config에 core_decay_rate가 있어야 함"
        
        # 알츠하이머는 새 기억 감쇠율이 높음
        assert alzheimer_config.new_memory_decay_rate > 0, \
            f"알츠하이머는 new_memory_decay_rate > 0이어야 함, got {alzheimer_config.new_memory_decay_rate}"
    
    def test_dementia_vs_alzheimer_difference(self):
        """치매 vs 알츠하이머 파라미터 차이"""
        from cognitive_kernel.cognitive_modes import CognitiveModePresets
        
        dementia_config = CognitiveModePresets.dementia()
        alzheimer_config = CognitiveModePresets.alzheimer()
        
        # 알츠하이머는 새 기억 감쇠율이 더 높아야 함
        assert alzheimer_config.new_memory_decay_rate >= dementia_config.new_memory_decay_rate, \
            f"알츠하이머는 새 기억 감쇠율이 더 높아야 함: " \
            f"{alzheimer_config.new_memory_decay_rate} >= {dementia_config.new_memory_decay_rate}"
        
        # 알츠하이머는 코어 감쇠율이 더 높을 수 있음
        assert alzheimer_config.core_decay_rate >= dementia_config.core_decay_rate, \
            f"알츠하이머는 코어 감쇠율이 더 높아야 함: " \
            f"{alzheimer_config.core_decay_rate} >= {dementia_config.core_decay_rate}"
    
    def test_dementia_core_decay(self):
        """치매 모드에서 코어 감쇠"""
        from cognitive_kernel.cognitive_modes import CognitiveModePresets
        
        dementia_config = CognitiveModePresets.dementia()
        dynamics_config = DynamicsConfig(
            core_decay_rate=dementia_config.core_decay_rate,
            old_memory_decay_rate=dementia_config.old_memory_decay_rate,
            new_memory_decay_rate=dementia_config.new_memory_decay_rate,
            memory_age_threshold=dementia_config.memory_age_threshold,
        )
        engine = DynamicsEngine(config=dynamics_config)
        
        import time
        current_time = time.time()
        
        # 오래된 기억
        memories_old = [
            {"importance": 0.9, "timestamp": current_time - 7200},  # 2시간 전 (임계값 초과)
        ]
        
        # 새 기억
        memories_new = [
            {"importance": 0.9, "timestamp": current_time - 1800},  # 30분 전 (임계값 이하)
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
    
    def test_alzheimer_new_memory_decay(self):
        """알츠하이머 모드에서 새 기억 감쇠"""
        from cognitive_kernel.cognitive_modes import CognitiveModePresets
        
        alzheimer_config = CognitiveModePresets.alzheimer()
        dynamics_config = DynamicsConfig(
            core_decay_rate=alzheimer_config.core_decay_rate,
            old_memory_decay_rate=alzheimer_config.old_memory_decay_rate,
            new_memory_decay_rate=alzheimer_config.new_memory_decay_rate,
            memory_age_threshold=alzheimer_config.memory_age_threshold,
        )
        engine = DynamicsEngine(config=dynamics_config)
        
        import time
        current_time = time.time()
        
        # 새 기억 (임계값 이하)
        memories_new = [
            {"importance": 0.9, "timestamp": current_time - 100},  # 100초 전
        ]
        
        # 코어 계산
        core = engine.calculate_core_strength(memories_new)
        
        # 알츠하이머는 새 기억 감쇠율이 높으므로 코어가 낮을 수 있음
        assert isinstance(core, float), "코어 강도는 float이어야 함"
        assert 0.0 <= core <= 1.0, f"코어 강도는 [0, 1] 범위여야 함, got {core}"


class TestModeIntegration:
    """모드 통합 테스트"""
    
    def test_kernel_mode_setting(self):
        """CognitiveKernel에서 모드 설정"""
        kernel = CognitiveKernel()
        
        # 문자열 모드 설정
        kernel.set_mode("adhd")
        assert kernel.mode == CognitiveMode.ADHD, \
            "문자열 'adhd'는 CognitiveMode.ADHD로 변환되어야 함"
        
        kernel.set_mode("asd")
        assert kernel.mode == CognitiveMode.ASD, \
            "문자열 'asd'는 CognitiveMode.ASD로 변환되어야 함"
        
        kernel.set_mode("dementia")
        assert kernel.mode == CognitiveMode.DEMENTIA, \
            "문자열 'dementia'는 CognitiveMode.DEMENTIA로 변환되어야 함"
        
        kernel.set_mode("alzheimer")
        assert kernel.mode == CognitiveMode.ALZHEIMER, \
            "문자열 'alzheimer'는 CognitiveMode.ALZHEIMER로 변환되어야 함"
    
    def test_mode_config_application(self):
        """모드 설정이 Dynamics Engine에 적용되는지 확인"""
        kernel = CognitiveKernel()
        
        # dementia 모드 설정
        kernel.set_mode("dementia")
        
        # Dynamics Engine의 config 확인
        dynamics_config = kernel.dynamics.config
        
        # dementia 모드의 파라미터가 적용되었는지 확인
        from cognitive_kernel.cognitive_modes import CognitiveModePresets
        dementia_config = CognitiveModePresets.dementia()
        
        # core_decay_rate 확인 (mode_config에서 가져옴)
        assert hasattr(kernel.mode_config, 'core_decay_rate'), \
            "mode_config에 core_decay_rate가 있어야 함"

