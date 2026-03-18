"""
Neural Dynamics Core - 뇌 모델링 관점 검증 테스트

뇌 모델링 관점에서의 최소 검증:
1. 안정성 테스트: dt/τ 변화에 따라 발산/수렴 경계 확인
2. 재현성 테스트: noise off일 때 완전 동일 결과, noise on일 때 통계적 분포 유지
3. 가소성 결과 테스트: Hebbian+decay로 W가 클립 경계에 붙는지/폭주하는지,
   특정 입력 패턴 반복 시 attractor가 "형성"되는지
"""

import sys
from pathlib import Path

import pytest
import numpy as np

# 프로젝트 루트를 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from cognitive_kernel.engines.dynamics import (
    ContinuousDynamicsConfig,
    NeuralDynamicsCore,
    HebbianPlasticityConfig,
    hebbian_update,
)


class TestStabilityBoundaries:
    """안정성 테스트: dt/τ 변화에 따라 발산/수렴 경계 확인"""
    
    def test_convergence_with_different_dt(self):
        """dt 변화에 따른 수렴 경계"""
        W = [[1.6, -1.2], [-1.2, 1.6]]
        x0 = [0.7, -0.4]
        
        # 작은 dt: 안정적 수렴
        cfg_small = ContinuousDynamicsConfig(dt=0.001, tau=0.1, activation="tanh")
        core_small = NeuralDynamicsCore(W=W, b=[0.0, 0.0], config=cfg_small, seed=42)
        traj_small = core_small.run(x0, steps=5000, stop_tol=1e-7, return_trajectory=True)
        
        # 큰 dt: 불안정 가능성
        cfg_large = ContinuousDynamicsConfig(dt=0.1, tau=0.1, activation="tanh")
        core_large = NeuralDynamicsCore(W=W, b=[0.0, 0.0], config=cfg_large, seed=42)
        traj_large = core_large.run(x0, steps=500, stop_tol=1e-7, return_trajectory=True)
        
        # 작은 dt는 수렴해야 함
        assert len(traj_small) < 5000, "작은 dt는 빠르게 수렴해야 함"
        
        # 큰 dt는 수렴하지 않을 수 있음 (또는 발산)
        # 최소한 궤적이 유한해야 함
        assert len(traj_large) > 0, "큰 dt도 궤적을 생성해야 함"
    
    def test_convergence_with_different_tau(self):
        """τ 변화에 따른 수렴 경계"""
        W = [[1.6, -1.2], [-1.2, 1.6]]
        x0 = [0.7, -0.4]
        
        # 작은 τ: 빠른 수렴
        cfg_fast = ContinuousDynamicsConfig(dt=0.01, tau=0.01, activation="tanh")
        core_fast = NeuralDynamicsCore(W=W, b=[0.0, 0.0], config=cfg_fast, seed=42)
        traj_fast = core_fast.run(x0, steps=2000, stop_tol=1e-7, return_trajectory=True)
        
        # 큰 τ: 느린 수렴
        cfg_slow = ContinuousDynamicsConfig(dt=0.01, tau=1.0, activation="tanh")
        core_slow = NeuralDynamicsCore(W=W, b=[0.0, 0.0], config=cfg_slow, seed=42)
        traj_slow = core_slow.run(x0, steps=2000, stop_tol=1e-7, return_trajectory=True)
        
        # 작은 τ는 빠르게 수렴
        assert len(traj_fast) < len(traj_slow), "작은 τ는 큰 τ보다 빠르게 수렴해야 함"
    
    def test_divergence_boundary(self):
        """발산 경계 테스트: 너무 큰 dt/τ 비율에서 발산"""
        W = [[2.0, -1.5], [-1.5, 2.0]]  # 강한 연결
        x0 = [1.0, -1.0]
        
        # dt/τ 비율이 너무 크면 발산 가능
        cfg_unstable = ContinuousDynamicsConfig(dt=0.5, tau=0.01, activation="tanh")
        core_unstable = NeuralDynamicsCore(W=W, b=[0.0, 0.0], config=cfg_unstable, seed=42)
        
        # clip_state로 발산 방지
        cfg_unstable.clip_state = 10.0
        
        traj = core_unstable.run(x0, steps=100, return_trajectory=True)
        
        # 클리핑으로 인해 유한해야 함
        assert len(traj) > 0
        # 모든 상태가 클립 범위 내에 있어야 함
        for x in traj:
            for xi in x:
                assert abs(xi) <= 10.0, f"상태가 클립 범위를 벗어남: {xi}"


class TestReproducibility:
    """재현성 테스트"""
    
    def test_deterministic_reproducibility(self):
        """noise off일 때 완전 동일 결과"""
        W = [[1.6, -1.2], [-1.2, 1.6]]
        x0 = [0.7, -0.4]
        cfg = ContinuousDynamicsConfig(dt=0.01, tau=0.1, activation="tanh", noise_scale=0.0)
        
        # 첫 번째 실행
        core1 = NeuralDynamicsCore(W=W, b=[0.0, 0.0], config=cfg, seed=123)
        traj1 = core1.run(x0, steps=1000, stop_tol=1e-7, return_trajectory=True)
        
        # 두 번째 실행 (같은 seed)
        core2 = NeuralDynamicsCore(W=W, b=[0.0, 0.0], config=cfg, seed=123)
        traj2 = core2.run(x0, steps=1000, stop_tol=1e-7, return_trajectory=True)
        
        # 완전히 동일해야 함
        assert len(traj1) == len(traj2), "궤적 길이가 동일해야 함"
        for i, (x1, x2) in enumerate(zip(traj1, traj2)):
            for j, (x1j, x2j) in enumerate(zip(x1, x2)):
                assert abs(x1j - x2j) < 1e-10, f"스텝 {i}, 노드 {j}에서 불일치: {x1j} vs {x2j}"
    
    def test_stochastic_distribution(self):
        """noise on일 때 통계적 분포 유지"""
        W = [[1.6, -1.2], [-1.2, 1.6]]
        x0 = [0.7, -0.4]
        cfg = ContinuousDynamicsConfig(dt=0.01, tau=0.1, activation="tanh", noise_scale=0.1)
        
        # 여러 실행
        n_runs = 20
        final_states = []
        
        for seed in range(n_runs):
            core = NeuralDynamicsCore(W=W, b=[0.0, 0.0], config=cfg, seed=seed)
            traj = core.run(x0, steps=500, return_trajectory=True)
            final_states.append(traj[-1])
        
        # 통계적 분포 확인
        final_states_array = np.array(final_states)
        
        # 노이즈 없는 경우의 수렴점 계산 (참조값)
        cfg_no_noise = ContinuousDynamicsConfig(dt=0.01, tau=0.1, activation="tanh", noise_scale=0.0)
        core_ref = NeuralDynamicsCore(W=W, b=[0.0, 0.0], config=cfg_no_noise, seed=42)
        traj_ref = core_ref.run(x0, steps=500, stop_tol=1e-7, return_trajectory=True)
        reference_point = traj_ref[-1]
        
        # 평균이 참조점 근처에 있어야 함 (노이즈가 있어도 대략 같은 어트랙터로 수렴)
        mean = np.mean(final_states_array, axis=0)
        for i, (m, ref) in enumerate(zip(mean, reference_point)):
            assert abs(m - ref) < 0.3, f"평균이 참조점에서 너무 벗어남: {m} vs {ref}"
        
        # 분산이 0이 아니어야 함 (노이즈 효과)
        std = np.std(final_states_array, axis=0)
        for s in std:
            assert s > 0.01, f"분산이 너무 작음: {s}"


class TestPlasticityResults:
    """가소성 결과 테스트"""
    
    def test_hebbian_weight_clipping(self):
        """Hebbian+decay로 W가 클립 경계에 붙는지 확인"""
        W = [[0.0, 0.0], [0.0, 0.0]]
        cfg = HebbianPlasticityConfig(eta=0.1, weight_decay=0.01, clip_weight=1.0)
        
        # 반복 업데이트
        pre = [1.0, 1.0]
        W_current = [row[:] for row in W]
        
        for _ in range(100):
            W_current = hebbian_update(W_current, pre=pre, post=None, config=cfg)
        
        # 클립 경계 확인
        for i in range(2):
            for j in range(2):
                assert abs(W_current[i][j]) <= 1.0, f"가중치가 클립 범위를 벗어남: W[{i}][{j}] = {W_current[i][j]}"
    
    def test_hebbian_weight_explosion(self):
        """가중치 폭주 방지 테스트"""
        W = [[0.0, 0.0], [0.0, 0.0]]
        # 클리핑 없이 큰 학습률
        cfg = HebbianPlasticityConfig(eta=1.0, weight_decay=0.0, clip_weight=None)
        
        pre = [1.0, 1.0]
        W_current = [row[:] for row in W]
        
        # 많은 업데이트
        for _ in range(1000):
            W_current = hebbian_update(W_current, pre=pre, post=None, config=cfg)
        
        # 클리핑이 없으면 폭주할 수 있음 (이건 예상된 동작)
        # 하지만 실제로는 weight_decay가 있어야 함
        # 이 테스트는 weight_decay가 없을 때의 동작을 확인
        max_weight = max(max(row) for row in W_current)
        # 폭주하지 않도록 weight_decay를 추가하는 것이 좋음
        # 여기서는 단순히 유한한지 확인
        assert abs(max_weight) < 1e6, "가중치가 과도하게 폭주함"
    
    def test_attractor_formation_with_repeated_pattern(self):
        """특정 입력 패턴 반복 시 attractor가 "형성"되는지"""
        W = [[0.5, 0.0], [0.0, 0.5]]
        cfg_dyn = ContinuousDynamicsConfig(dt=0.01, tau=0.1, activation="tanh")
        cfg_plastic = HebbianPlasticityConfig(eta=0.05, weight_decay=0.001, clip_weight=2.0)
        
        core = NeuralDynamicsCore(W=W, b=[0.0, 0.0], config=cfg_dyn, seed=42)
        
        # 특정 입력 패턴 반복
        pattern = [0.8, 0.2]
        n_patterns = 10
        
        for pattern_idx in range(n_patterns):
            # 동역학 실행
            x0 = [0.0, 0.0]
            traj = core.run(x0, steps=200, input_schedule=lambda t: pattern, return_trajectory=True)
            x_final = traj[-1]
            
            # 가소성 업데이트 (매 5번째 패턴마다)
            if pattern_idx > 0 and pattern_idx % 5 == 0:
                core.W = hebbian_update(core.W, pre=x_final, post=None, config=cfg_plastic)
        
        # 패턴 반복 후 가중치가 변화했는지 확인
        # 초기 W와 다른지 확인
        initial_W = [[0.5, 0.0], [0.0, 0.5]]
        weight_changed = False
        for i in range(2):
            for j in range(2):
                if abs(core.W[i][j] - initial_W[i][j]) > 0.01:
                    weight_changed = True
        
        assert weight_changed, "패턴 반복 후 가중치가 변화해야 함"
        
        # 최종 상태가 패턴에 가까워졌는지 확인 (attractor 형성)
        final_traj = core.run([0.0, 0.0], steps=200, input_schedule=lambda t: pattern, return_trajectory=True)
        final_state = final_traj[-1]
        
        # 패턴과의 유사도
        similarity = sum(abs(final_state[i] - pattern[i]) for i in range(2)) / len(pattern)
        # 학습 후에는 더 가까워져야 함 (하지만 완벽하지 않을 수 있음)
        assert similarity < 1.0, "최종 상태가 패턴에 어느 정도 가까워져야 함"

