"""
Basal Ganglia Engine Basic Usage Example
기저핵 엔진 기본 사용 예제

Author: GNJz (Qquarts)
Version: 1.0.0-alpha
"""

from basal_ganglia import BasalGangliaEngine, BasalGangliaConfig, ActionType


def main():
    print("=" * 70)
    print("🧠 Basal Ganglia Engine - Basic Usage Example")
    print("=" * 70)
    
    # =========================================================
    # 1. 엔진 초기화
    # =========================================================
    print("\n[1] 엔진 초기화")
    print("-" * 70)
    
    engine = BasalGangliaEngine()
    print("✓ Basal Ganglia Engine 초기화 완료")
    
    # =========================================================
    # 2. 행동 선택 (초기 상태)
    # =========================================================
    print("\n[2] 행동 선택 (초기 상태)")
    print("-" * 70)
    
    context = "인사 상황"
    possible_actions = ["안녕하세요", "반갑습니다", "하이"]
    
    result = engine.select_action(context, possible_actions)
    print(f"상황: '{context}'")
    print(f"가능한 행동: {possible_actions}")
    print(f"선택된 행동: '{result.action.name}'")
    print(f"결정: {result.decision.value}")
    print(f"확신도: {result.confidence:.2f}")
    print(f"자동 실행: {result.is_automatic}")
    print(f"이유: {result.reasoning}")
    
    # =========================================================
    # 3. 학습 (보상 기반)
    # =========================================================
    print("\n[3] 학습 (보상 기반)")
    print("-" * 70)
    
    print("20회 학습 진행 중...")
    for i in range(20):
        # "안녕하세요"에 높은 보상
        engine.learn(context, "안녕하세요", reward=0.8)
        # 다른 행동에 낮은 보상
        engine.learn(context, "하이", reward=0.2)
    
    print("\n학습 후 Q-값:")
    for action_name in possible_actions:
        best_action = engine.get_best_action(context)
        if best_action and best_action.name == action_name:
            action = engine.q_table[engine._normalize_context(context)][action_name]
            print(f"  '{action_name}': Q={action.q_value:.2f}, "
                  f"실행횟수={action.execution_count}, "
                  f"습관강도={action.habit_strength:.2f}")
    
    # =========================================================
    # 4. 습관 형성
    # =========================================================
    print("\n[4] 습관 형성")
    print("-" * 70)
    
    print("추가 30회 학습 진행 중...")
    for i in range(30):
        engine.learn(context, "안녕하세요", reward=0.9)
    
    habits = engine.get_habits()
    print(f"\n형성된 습관: {len(habits)}개")
    for h in habits:
        print(f"  '{h.context}' → '{h.name}' (강도: {h.habit_strength:.2f})")
    
    # =========================================================
    # 5. 습관화 후 행동 선택
    # =========================================================
    print("\n[5] 습관화 후 행동 선택")
    print("-" * 70)
    
    result = engine.select_action(context, possible_actions)
    print(f"선택된 행동: '{result.action.name}'")
    print(f"자동 실행: {result.is_automatic}")
    print(f"이유: {result.reasoning}")
    
    # =========================================================
    # 6. 도파민 상태
    # =========================================================
    print("\n[6] 도파민 상태")
    print("-" * 70)
    
    print(f"현재 도파민 레벨: {engine.dopamine_level:.2f}")
    
    # 도파민 주입
    engine.set_dopamine_level(0.8)
    print(f"도파민 주입 후: {engine.dopamine_level:.2f}")
    
    # =========================================================
    # 7. 전체 상태
    # =========================================================
    print("\n[7] 전체 상태")
    print("-" * 70)
    
    state = engine.get_state()
    print(f"도파민: {state['dopamine']}")
    print(f"총 컨텍스트: {state['total_contexts']}")
    print(f"총 행동: {state['total_actions']}")
    print(f"습관 수: {len(state['habits'])}")
    print(f"\n통계:")
    for key, value in state['stats'].items():
        print(f"  {key}: {value}")
    
    # =========================================================
    # 8. 커스텀 설정 예제
    # =========================================================
    print("\n[8] 커스텀 설정 예제")
    print("-" * 70)
    
    custom_config = BasalGangliaConfig(
        alpha=0.15,          # 학습률 증가
        gamma=0.95,          # 미래 보상 중시
        habit_threshold=0.8, # 습관화 임계값 증가
        impulsivity=0.7,     # 충동성 높음 (탐색↑)
    )
    
    custom_engine = BasalGangliaEngine(config=custom_config)
    print("✓ 커스텀 설정 엔진 초기화 완료")
    print(f"  학습률: {custom_engine.config.alpha}")
    print(f"  할인율: {custom_engine.config.gamma}")
    print(f"  습관 임계값: {custom_engine.config.habit_threshold}")
    print(f"  소프트맥스 온도: {custom_engine.config.tau:.2f} (충동성 적용)")
    
    print("\n" + "=" * 70)
    print("✅ 예제 실행 완료!")
    print("=" * 70)


if __name__ == '__main__':
    main()

