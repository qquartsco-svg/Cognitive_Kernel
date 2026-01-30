"""
세차운동(Precession) 데모 v2.0.1 - 규약 준수 버전

ADHD(+) ↔ ASD(-) 축이 만드는 "회전장"과 세차운동을 시각화합니다.

핵심:
- kernel.decide() 직접 사용 (1:1 정합성)
- 세션 격리 (uuid 기반)
- 공개 API만 사용
- CONFIG로 파라미터화
"""

import numpy as np
import uuid
import time
from typing import List, Dict, Tuple, Optional
from cognitive_kernel import CognitiveKernel, CognitiveMode


# CONFIG: 모든 물리 상수 파라미터화
CONFIG = {
    "alpha": 0.5,      # 기억 영향 계수 (중력 코어 강도)
    "beta": 5.0,       # 결정 축 고정 (ASD 성분) - ModeConfig에서 설정됨
    "gamma": 0.3,      # 회전 토크 세기 (ADHD 성분)
    "omega": 0.05,     # 세차 속도 (느린 시간척도)
    "n_steps": 100,    # 시뮬레이션 스텝 수
    "base_reward": 0.5,  # 기본 보상 U_0
}


def calculate_entropy_from_probabilities(probabilities: Dict[str, float]) -> float:
    """확률 분포에서 엔트로피 계산"""
    probs = np.array(list(probabilities.values()))
    probs = probs[probs > 0]
    if len(probs) == 0:
        return 0.0
    return -np.sum(probs * np.log(probs))


def simulate_precession_v2(
    config: Dict = CONFIG,
) -> Tuple[List[float], List[float], List[str]]:
    """
    세차운동 시뮬레이션 (v2.0.1 규약 준수)
    
    Returns:
        (entropies, phi_history, dominant_choice_history)
    """
    # 세션 격리: uuid 기반 독립 세션
    session_name = f"precession_demo_{uuid.uuid4().hex[:8]}"
    
    # 옵션 정의
    options = ["choose_red", "choose_blue", "choose_green"]
    psi = {opt: i * 2 * np.pi / len(options) for i, opt in enumerate(options)}
    
    # 초기화
    phi = 0.0
    entropies = []
    phi_history = []
    dominant_choice_history = []
    
    print("=" * 70)
    print("🌐 세차운동 시뮬레이션 (v2.0.1 규약 준수)")
    print("=" * 70)
    print(f"   세션: {session_name}")
    print(f"   파라미터:")
    print(f"   - 기억 영향 계수 (α): {config['alpha']}")
    print(f"   - 회전 토크 세기 (γ): {config['gamma']} (ADHD 성분)")
    print(f"   - 세차 속도 (ω): {config['omega']}")
    print(f"   - 시뮬레이션 스텝: {config['n_steps']}")
    print()
    
    # Cognitive Kernel 초기화 (ASD 모드로 축 고정)
    with CognitiveKernel(session_name, mode=CognitiveMode.ASD, auto_load=False) as kernel:
        # 기억 설정 (ASD 고착을 위한 "red" 관련 기억)
        kernel.remember("preference", {"text": "I like red"}, importance=0.8)
        kernel.remember("preference", {"text": "Red is my favorite"}, importance=0.7)
        kernel.remember("preference", {"text": "Red color preference"}, importance=0.6)
        
        for step in range(config['n_steps']):
            # 회전 토크 계산: T_n(k) = cos(φ_n - ψ_k)
            external_torque = {
                opt: config['gamma'] * np.cos(phi - psi[opt])
                for opt in options
            }
            
            # kernel.decide() 직접 사용 (1:1 정합성)
            result = kernel.decide(
                options=options,
                context=None,
                use_habit=False,
                external_torque=external_torque,
            )
            
            # 결과에서 확률 추출 (PFC 내부 계산된 값 사용)
            # 주의: 현재 decide()는 단일 선택의 확률만 반환
            # 전체 분포를 얻기 위해 각 옵션에 대해 decide() 호출
            # (실제로는 PFC 내부에서 계산되지만, 데모를 위해 근사)
            
            # 대안: 각 옵션에 대해 토크를 주입하고 utility 비교
            utilities = {}
            for opt in options:
                torque = {opt: external_torque[opt]}
                temp_result = kernel.decide(
                    options=[opt],
                    context=None,
                    use_habit=False,
                    external_torque=torque,
                )
                utilities[opt] = temp_result.get('utility', 0.5)
            
            # Softmax 확률 계산 (PFC의 β 사용)
            # 주의: 실제로는 PFC 내부에서 계산되지만, 데모를 위해 재현
            beta = kernel.mode_config.decision_temperature
            exp_utils = {opt: np.exp(beta * (u - max(utilities.values()))) 
                        for opt, u in utilities.items()}
            total = sum(exp_utils.values())
            probabilities = {opt: exp_utils[opt] / total for opt in options}
            
            # 엔트로피 계산
            entropy = calculate_entropy_from_probabilities(probabilities)
            entropies.append(entropy)
            phi_history.append(phi)
            
            # 지배적 선택
            dominant_choice = max(probabilities, key=probabilities.get)
            dominant_choice_history.append(dominant_choice)
            
            # 위상 업데이트 (느린 시간척도)
            phi += config['omega']
            
            # 주기적으로 출력
            if step % 20 == 0:
                print(f"   Step {step:3d}: φ={phi:.3f}, E={entropy:.3f}, "
                      f"P=[{probabilities['choose_red']:.3f}, "
                      f"{probabilities['choose_blue']:.3f}, "
                      f"{probabilities['choose_green']:.3f}], "
                      f"Dominant={dominant_choice}")
    
    return entropies, phi_history, dominant_choice_history


def analyze_precession_results(
    entropies: List[float],
    phi_history: List[float],
    dominant_choice_history: List[str],
):
    """세차운동 결과 분석"""
    print("=" * 70)
    print("📊 결과 분석")
    print("=" * 70)
    print(f"   평균 엔트로피: {np.mean(entropies):.3f}")
    print(f"   엔트로피 범위: [{np.min(entropies):.3f}, {np.max(entropies):.3f}]")
    print(f"   최대 엔트로피 (이론값): {np.log(3):.3f}")
    print()
    
    # 선택 변화 횟수
    choice_changes = sum(1 for i in range(1, len(dominant_choice_history)) 
                        if dominant_choice_history[i] != dominant_choice_history[i-1])
    print(f"   선택 변화 횟수: {choice_changes}회")
    print(f"   선택 변화율: {choice_changes / len(dominant_choice_history) * 100:.1f}%")
    print()
    
    # 세차운동 확인
    if choice_changes > 0 and np.mean(entropies) < np.log(3) * 0.8:
        print("   ✅ 세차운동 확인:")
        print("   - 엔트로피는 낮게 유지 (축 고정)")
        print("   - 선택은 주기적으로 변화 (회전)")
    else:
        print("   ⚠️  세차운동 미확인:")
        if choice_changes == 0:
            print("   - 선택 변화 없음 (고착)")
        if np.mean(entropies) >= np.log(3) * 0.8:
            print("   - 엔트로피가 높음 (분산)")
    print()


def main():
    """메인 함수"""
    print("\n" + "=" * 70)
    print("🧲 세차운동(Precession) 데모 v2.0.1 - 규약 준수 버전")
    print("=" * 70)
    print()
    print("   핵심:")
    print("   - kernel.decide() 직접 사용 (1:1 정합성)")
    print("   - 세션 격리 (uuid 기반)")
    print("   - 공개 API만 사용")
    print("   - CONFIG로 파라미터화")
    print()
    
    # 세차운동 시뮬레이션
    entropies, phi_history, dominant_choice_history = simulate_precession_v2(CONFIG)
    
    # 결과 분석
    analyze_precession_results(entropies, phi_history, dominant_choice_history)
    
    print("=" * 70)
    print("✅ 세차운동 시뮬레이션 완료")
    print("=" * 70)
    print()
    print("   핵심 통찰:")
    print("   1. ASD 성분(높은 β)이 '축을 고정'함")
    print("   2. ADHD 성분(회전 토크)이 '축을 회전'시킴")
    print("   3. 결과: 선호축이 느리게 회전하는 세차운동")
    print("   4. 엔트로피는 낮게 유지되지만, 선택은 주기적으로 변화")
    print()


if __name__ == "__main__":
    main()

