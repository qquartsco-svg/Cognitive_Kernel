"""
안정 코어(Stability Core) 데모

정신이 무너지지 않고 유지되는 최소 동역학 조건을 시뮬레이션합니다.

핵심 개념:
- 중력 코어 (기억 중력 αC + 결정 축 고정 β)
- 회전장 (비보존 회전장)
- 세차 자유도 (느린 회전)
"""

import numpy as np
from typing import List, Dict, Tuple
from cognitive_kernel import CognitiveKernel, CognitiveMode


def calculate_entropy(probabilities: List[float]) -> float:
    """엔트로피 계산"""
    probs = np.array(probabilities)
    probs = probs[probs > 0]
    return -np.sum(probs * np.log(probs))


def simulate_stability_core(
    n_steps: int = 100,
    alpha: float = 0.5,      # 기억 영향 계수 (중력 코어 강도)
    beta: float = 3.0,       # 결정 축 고정 (ASD 성분)
    gamma: float = 0.2,     # 회전 토크 (ADHD 성분, 세차 자유도)
    omega: float = 0.03,     # 세차 속도
    perturbation_steps: List[int] = [30, 60],  # 외란 주입 시점
) -> Tuple[List[float], List[float], List[int]]:
    """
    안정 코어 시뮬레이션
    
    Args:
        n_steps: 시뮬레이션 스텝 수
        alpha: 기억 영향 계수 (중력 코어 강도)
        beta: 결정 축 고정 (ASD 성분)
        gamma: 회전 토크 (ADHD 성분)
        omega: 세차 속도
        perturbation_steps: 외란 주입 시점
    
    Returns:
        (entropies, core_strength_history, dominant_choice_history)
    """
    options = ["choose_red", "choose_blue", "choose_green"]
    psi = [0.0, 2 * np.pi / 3, 4 * np.pi / 3]
    
    # 초기화
    phi = 0.0
    entropies = []
    core_strength_history = []
    dominant_choice_history = []
    
    # 기억 설정 (중력 코어 형성)
    kernel = CognitiveKernel("stability_core_demo", mode=CognitiveMode.ASD)
    kernel.remember("preference", {"text": "I like red"}, importance=0.8)
    kernel.remember("preference", {"text": "Red is my favorite"}, importance=0.7)
    kernel.remember("preference", {"text": "Red color preference"}, importance=0.6)
    
    print("=" * 70)
    print("🧲 안정 코어 시뮬레이션")
    print("=" * 70)
    print(f"   파라미터:")
    print(f"   - 중력 코어 강도 (α): {alpha}")
    print(f"   - 결정 축 고정 (β): {beta} (ASD 성분)")
    print(f"   - 회전 토크 (γ): {gamma} (ADHD 성분, 세차 자유도)")
    print(f"   - 세차 속도 (ω): {omega}")
    print(f"   - 외란 주입 시점: {perturbation_steps}")
    print()
    
    for step in range(n_steps):
        # 외란 주입 (안정 루프 흐트러뜨리기)
        if step in perturbation_steps:
            # 새로운 기억 추가 (그래프 재배치)
            kernel.remember("new_preference", {"text": "I also like blue"}, importance=0.5)
            print(f"   ⚡ Step {step}: 외란 주입 (새 기억 추가)")
        
        # 기억 회상
        memories = kernel.recall(k=3)
        
        # 중력 코어 강도 계산 (αC)
        core_strength = 0.0
        for mem in memories:
            core_strength += mem.get("importance", 0.0)
        core_strength = min(1.0, core_strength / len(memories)) if memories else 0.0
        core_strength_history.append(core_strength)
        
        # 각 옵션에 대한 utility 계산
        utilities = []
        for i, opt in enumerate(options):
            # 키워드 추출
            opt_keywords = kernel._extract_keywords(opt)
            
            # 기억 관련성 (C_n(k))
            memory_relevance = kernel._calculate_memory_relevance(opt_keywords, memories)
            
            # 기본 utility (U_0 + α * C_n(k)) - 중력 코어
            base_utility = 0.5 + alpha * memory_relevance
            
            # 회전 토크 (T_n(k) = cos(φ_n - ψ_k)) - 세차 자유도
            torque = np.cos(phi - psi[i])
            
            # 최종 utility (U_n,k = U_0 + α * C_n(k) + γ * T_n(k))
            utility = base_utility + gamma * torque
            utilities.append(utility)
        
        # Softmax 확률 계산 (β = 결정 축 고정)
        utilities = np.array(utilities)
        exp_utils = np.exp(beta * (utilities - np.max(utilities)))
        probabilities = exp_utils / np.sum(exp_utils)
        
        # 엔트로피 계산
        entropy = calculate_entropy(probabilities)
        entropies.append(entropy)
        
        # 지배적 선택
        dominant_idx = np.argmax(probabilities)
        dominant_choice_history.append(dominant_idx)
        
        # 위상 업데이트 (느린 시간척도)
        phi += omega
        
        # 주기적으로 출력
        if step % 20 == 0 or step in perturbation_steps:
            print(f"   Step {step:3d}: φ={phi:.3f}, Core={core_strength:.3f}, "
                  f"E={entropy:.3f}, Dominant={options[dominant_idx]}")
    
    return entropies, core_strength_history, dominant_choice_history


def analyze_stability(
    entropies: List[float],
    core_strength_history: List[float],
    dominant_choice_history: List[int],
):
    """안정성 분석"""
    print("=" * 70)
    print("📊 안정성 분석")
    print("=" * 70)
    
    # 1. 엔트로피 안정성
    entropy_mean = np.mean(entropies)
    entropy_std = np.std(entropies)
    print(f"   엔트로피:")
    print(f"   - 평균: {entropy_mean:.3f}")
    print(f"   - 표준편차: {entropy_std:.3f}")
    print(f"   - 범위: [{np.min(entropies):.3f}, {np.max(entropies):.3f}]")
    
    # 안정성 판단
    if entropy_std < 0.2:
        print(f"   ✅ 엔트로피 안정 (표준편차 < 0.2)")
    else:
        print(f"   ⚠️  엔트로피 불안정 (표준편차 >= 0.2)")
    
    print()
    
    # 2. 코어 강도 안정성
    core_mean = np.mean(core_strength_history)
    core_std = np.std(core_strength_history)
    print(f"   코어 강도:")
    print(f"   - 평균: {core_mean:.3f}")
    print(f"   - 표준편차: {core_std:.3f}")
    
    if core_mean > 0.5:
        print(f"   ✅ 코어 강도 충분 (평균 > 0.5)")
    else:
        print(f"   ⚠️  코어 강도 부족 (평균 <= 0.5)")
    
    print()
    
    # 3. 선택 변화 (세차 자유도)
    choice_changes = sum(1 for i in range(1, len(dominant_choice_history)) 
                        if dominant_choice_history[i] != dominant_choice_history[i-1])
    change_rate = choice_changes / len(dominant_choice_history) * 100
    
    print(f"   선택 변화:")
    print(f"   - 변화 횟수: {choice_changes}회")
    print(f"   - 변화율: {change_rate:.1f}%")
    
    if 2.0 <= change_rate <= 10.0:
        print(f"   ✅ 세차 자유도 적절 (2% ~ 10%)")
    elif change_rate < 2.0:
        print(f"   ⚠️  세차 자유도 부족 (고착)")
    else:
        print(f"   ⚠️  세차 자유도 과다 (불안정)")
    
    print()
    
    # 4. 전체 안정성 판단
    print("=" * 70)
    print("🎯 전체 안정성 판단")
    print("=" * 70)
    
    stability_score = 0
    
    if entropy_std < 0.2:
        stability_score += 1
    if core_mean > 0.5:
        stability_score += 1
    if 2.0 <= change_rate <= 10.0:
        stability_score += 1
    
    if stability_score == 3:
        print("   ✅ 안정 코어 형성 성공!")
        print("   - 엔트로피 안정")
        print("   - 코어 강도 충분")
        print("   - 세차 자유도 적절")
    elif stability_score == 2:
        print("   ⚠️  부분적 안정")
    else:
        print("   ❌ 안정 코어 형성 실패")
        print("   - 정신 붕괴 위험")
    
    print()


def main():
    """메인 함수"""
    print("\n" + "=" * 70)
    print("🧲 안정 코어(Stability Core) 데모")
    print("=" * 70)
    print()
    print("   개념:")
    print("   - 중력 코어 (기억 중력 αC + 결정 축 고정 β)")
    print("   - 회전장 (비보존 회전장)")
    print("   - 세차 자유도 (느린 회전)")
    print("   - 정신 안정 = 코어 × 회전장 × 세차 자유도")
    print()
    
    # 안정 코어 시뮬레이션
    entropies, core_strength_history, dominant_choice_history = simulate_stability_core(
        n_steps=100,
        alpha=0.5,      # 중력 코어 강도
        beta=3.0,       # 결정 축 고정
        gamma=0.2,      # 회전 토크
        omega=0.03,     # 세차 속도
        perturbation_steps=[30, 60],  # 외란 주입
    )
    
    # 안정성 분석
    analyze_stability(entropies, core_strength_history, dominant_choice_history)
    
    print("=" * 70)
    print("✅ 안정 코어 시뮬레이션 완료")
    print("=" * 70)
    print()
    print("   핵심 통찰:")
    print("   1. 정신은 '고정'으로 유지되지 않는다")
    print("   2. 정신은 '돌면서' 유지된다")
    print("   3. 중력 코어 + 회전장 + 세차 자유도 = 안정")
    print("   4. 외란 주입 후 재조합 과정에서 창발 발생")
    print()


if __name__ == "__main__":
    main()

