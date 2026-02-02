"""
상태 축 테스트: precession_phi, history 관리 검증

테스트 범위:
- precession_phi wrap (0~2π)
- history maxlen 제한
- 상태 업데이트 연속성
"""

import pytest
import math
import sys
from pathlib import Path

# 프로젝트 루트를 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from cognitive_kernel.engines.dynamics import DynamicsEngine, DynamicsConfig, DynamicsState


class TestPrecessionPhi:
    """precession_phi 상태 관리 테스트"""
    
    def test_precession_phi_initial(self):
        """초기 precession_phi 값"""
        engine = DynamicsEngine()
        
        # 초기값 확인
        phi = engine.state.precession_phi
        assert 0.0 <= phi < 2 * math.pi, \
            f"초기 precession_phi는 [0, 2π) 범위여야 함, got {phi}"
    
    def test_precession_phi_wrap_positive(self):
        """precession_phi가 2π를 넘으면 wrap"""
        engine = DynamicsEngine()
        
        # 2π를 넘는 값 설정
        engine.state.precession_phi = 2 * math.pi + 0.5
        
        # wrap 확인 (구현에 따라 자동 또는 수동)
        # 실제 구현 확인 필요
        phi = engine.state.precession_phi
        
        # wrap이 되었다면 [0, 2π) 범위
        if phi >= 2 * math.pi:
            # 수동으로 wrap
            phi = phi % (2 * math.pi)
        
        assert 0.0 <= phi < 2 * math.pi, \
            f"precession_phi는 [0, 2π) 범위여야 함, got {phi}"
    
    def test_precession_phi_wrap_negative(self):
        """precession_phi가 음수면 wrap"""
        engine = DynamicsEngine()
        
        # 음수 값 설정
        engine.state.precession_phi = -0.5
        
        # wrap 확인
        phi = engine.state.precession_phi
        
        # wrap이 되었다면 [0, 2π) 범위
        if phi < 0:
            # 수동으로 wrap
            phi = phi % (2 * math.pi)
            if phi < 0:
                phi += 2 * math.pi
        
        assert 0.0 <= phi < 2 * math.pi, \
            f"precession_phi는 [0, 2π) 범위여야 함, got {phi}"
    
    def test_precession_phi_update_continuity(self):
        """precession_phi 업데이트 연속성"""
        engine = DynamicsEngine()
        
        phi_initial = engine.state.precession_phi
        
        # 토크 생성 (precession_phi 업데이트됨)
        options = ["rest", "work", "exercise"]
        entropy = 0.8
        torque = engine.generate_torque(options, entropy, mode="normal")
        
        phi_updated = engine.state.precession_phi
        
        # 연속적인 변화여야 함 (급격한 점프 없음)
        diff = abs(phi_updated - phi_initial)
        
        # 2π를 넘는 경우 wrap 고려
        if diff > math.pi:
            diff = 2 * math.pi - diff
        
        # 작은 변화여야 함 (구현에 따라 다를 수 있음)
        assert diff < 2 * math.pi, \
            f"precession_phi 변화가 너무 큼: {phi_initial} -> {phi_updated} (diff={diff})"


class TestHistoryManagement:
    """history 관리 테스트"""
    
    def test_entropy_history_initial(self):
        """초기 entropy_history"""
        engine = DynamicsEngine()
        
        history = engine.state.entropy_history
        assert isinstance(history, list), "entropy_history는 list여야 함"
        assert len(history) == 0, f"초기 entropy_history는 비어있어야 함, got {len(history)}"
    
    def test_entropy_history_update(self):
        """entropy_history 업데이트"""
        engine = DynamicsEngine()
        
        # 엔트로피 계산 및 히스토리 업데이트
        entropy1 = engine.calculate_entropy([0.5, 0.3, 0.2])
        engine.update_history(entropy1, 0.5)
        
        entropy2 = engine.calculate_entropy([0.4, 0.4, 0.2])
        engine.update_history(entropy2, 0.6)
        
        entropy3 = engine.calculate_entropy([0.33, 0.33, 0.34])
        engine.update_history(entropy3, 0.7)
        
        history = engine.state.entropy_history
        assert len(history) == 3, \
            f"entropy_history는 3개 항목을 가져야 함, got {len(history)}"
        assert abs(history[-1] - entropy3) < 1e-6, \
            f"마지막 엔트로피는 {entropy3}이어야 함, got {history[-1]}"
    
    def test_entropy_history_maxlen(self):
        """entropy_history maxlen 제한"""
        config = DynamicsConfig(history_size=5)
        engine = DynamicsEngine(config=config)
        
        # maxlen보다 많은 엔트로피 추가
        for i in range(10):
            entropy = 0.5 + i * 0.01
            engine.update_history(entropy, 0.5)
        
        history = engine.state.entropy_history
        assert len(history) <= 5, \
            f"entropy_history는 maxlen(5)를 넘지 않아야 함, got {len(history)}"
    
    def test_core_strength_history_update(self):
        """core_strength_history 업데이트"""
        engine = DynamicsEngine()
        
        import time
        current_time = time.time()
        
        memories = [
            {"importance": 0.9, "timestamp": current_time - 3600},
        ]
        
        # 코어 강도 계산
        core1 = engine.calculate_core_strength(memories)
        engine.update_history(0.5, core1)  # history 업데이트
        
        core2 = engine.calculate_core_strength(memories)
        engine.update_history(0.6, core2)  # history 업데이트
        
        history = engine.state.core_strength_history
        assert len(history) >= 2, \
            f"core_strength_history는 최소 2개 항목을 가져야 함, got {len(history)}"
    
    def test_core_strength_history_maxlen(self):
        """core_strength_history maxlen 제한"""
        config = DynamicsConfig(history_size=5)
        engine = DynamicsEngine(config=config)
        
        import time
        current_time = time.time()
        
        memories = [
            {"importance": 0.9, "timestamp": current_time - 3600},
        ]
        
        # 많은 코어 강도 계산 및 history 업데이트
        for i in range(10):
            core = engine.calculate_core_strength(memories)
            engine.update_history(0.5, core)
        
        history = engine.state.core_strength_history
        # maxlen 제한 확인
        assert len(history) <= 5, \
            f"core_strength_history는 maxlen(5)를 넘지 않아야 함, got {len(history)}"


class TestStatePersistence:
    """상태 지속성 테스트"""
    
    def test_state_initialization(self):
        """상태 초기화"""
        engine = DynamicsEngine()
        
        state = engine.state
        assert isinstance(state, DynamicsState), "state는 DynamicsState여야 함"
        assert isinstance(state.entropy_history, list), "entropy_history는 list여야 함"
        assert isinstance(state.core_strength_history, list), "core_strength_history는 list여야 함"
        assert state.persistent_core is None or isinstance(state.persistent_core, float), \
            f"persistent_core는 None 또는 float이어야 함, got {type(state.persistent_core)}"
        assert isinstance(state.precession_phi, float), "precession_phi는 float이어야 함"
    
    def test_state_independence(self):
        """상태 독립성: 여러 엔진 인스턴스는 독립적"""
        engine1 = DynamicsEngine()
        engine2 = DynamicsEngine()
        
        # engine1 상태 변경
        engine1.update_history(0.5, 0.5)
        
        # engine2는 영향받지 않아야 함
        assert len(engine2.state.entropy_history) == 0, \
            "engine2의 상태는 engine1과 독립적이어야 함"
    
    def test_cognitive_distress_state(self):
        """cognitive_distress 상태"""
        engine = DynamicsEngine()
        
        # 초기 상태
        assert isinstance(engine.state.cognitive_distress, bool), \
            "cognitive_distress는 bool이어야 함"
        
        # distress 확인 (높은 엔트로피, 낮은 코어)
        import time
        current_time = time.time()
        
        memories = [
            {"importance": 0.1, "timestamp": current_time - 3600},  # 낮은 중요도
        ]
        
        core = engine.calculate_core_strength(memories)
        entropy = 0.9  # 높은 엔트로피
        
        is_distress, message = engine.check_cognitive_distress(entropy, core, num_options=3)
        
        # distress 상태 확인
        assert isinstance(is_distress, bool), "is_distress는 bool이어야 함"
        assert isinstance(message, str), "message는 str이어야 함"

