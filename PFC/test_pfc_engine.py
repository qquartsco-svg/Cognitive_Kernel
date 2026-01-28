"""PFC Engine v1.0 테스트 스크립트.

실행:
    cd /Users/jazzin/Desktop/00_BRAIN/Cognitive_Kernel
    python PFC/test_pfc_engine.py
"""

import sys
from pathlib import Path

# 패키지 경로 추가
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "package"))

from pfc import PFCEngine, PFCConfig, Action


def main() -> None:
    print("=" * 60)
    print("PFC Engine v1.0 - Test (영사기 + 감독)")
    print("=" * 60)

    # 1. 엔진 초기화
    config = PFCConfig(
        working_memory_capacity=5,
        risk_aversion=0.5,
        inhibition_threshold=0.6,
        decision_temperature=2.0,
    )
    pfc = PFCEngine(config)

    # 2. Working Memory 테스트
    print("\n[1] Working Memory 테스트 (Miller's Law: 용량 5)")
    
    # MemoryRank 결과 시뮬레이션
    top_memories = [
        ("memory_trauma_001", 0.45),
        ("memory_yesterday_lunch", 0.30),
        ("memory_friend_call", 0.25),
        ("memory_work_task", 0.20),
        ("memory_random", 0.10),
        ("memory_overflow", 0.05),  # 이건 eviction 대상
    ]
    
    pfc.load_from_memoryrank(top_memories)
    wm = pfc.get_working_memory()
    print(f"  로드된 기억 수: {len(wm)} (용량: {config.working_memory_capacity})")
    for slot in wm:
        print(f"    - {slot.content['memory_id']}: relevance={slot.relevance:.3f}")

    # 3. 행동 후보 생성
    print("\n[2] 행동 후보 효용 평가")
    actions = [
        Action.create("rest", reward=0.6, cost=0.1, risk=0.05),
        Action.create("work", reward=0.8, cost=0.5, risk=0.2),
        Action.create("socialize", reward=0.7, cost=0.3, risk=0.1),
        Action.create("risky_adventure", reward=0.9, cost=0.4, risk=0.8),
    ]

    for action in actions:
        utility = pfc.evaluate_action(action)
        print(f"  {action.name}: U = {utility:.3f} (r={action.expected_reward}, c={action.effort_cost}, risk={action.risk})")

    # 4. 억제 테스트
    print("\n[3] 억제(Inhibition) 테스트")
    risky_action = actions[3]  # risky_adventure
    inhibit, conflict = pfc.should_inhibit(risky_action, actions[:3])
    print(f"  '{risky_action.name}' 억제 여부: {inhibit}")
    print(f"  갈등 신호: {conflict:.3f} (threshold: {config.inhibition_threshold})")

    # 5. Softmax 선택 테스트
    print("\n[4] Softmax 행동 선택")
    safe_actions = actions[:3]  # risky_adventure 제외
    utilities = [pfc.evaluate_action(a) for a in safe_actions]
    probs = pfc.softmax_probabilities(utilities)
    
    print(f"  선택 확률 (temperature={config.decision_temperature}):")
    for a, p in zip(safe_actions, probs):
        print(f"    {a.name}: {p:.1%}")

    # 6. 통합 파이프라인 테스트
    print("\n[5] 통합 파이프라인 (process)")
    result = pfc.process(
        candidate_actions=actions,
        goal="complete daily tasks",
        goal_priority=0.7,
        deterministic=True,  # argmax 선택
    )

    if result.inhibited:
        print(f"  결과: 억제됨 (conflict={result.conflict_signal:.3f})")
    else:
        print(f"  선택된 행동: {result.action.name}")
        print(f"  효용: {result.utility:.3f}")
        print(f"  선택 확률: {result.selection_probability:.1%}")
        print(f"  갈등 신호: {result.conflict_signal:.3f}")

    # 7. 상태 확인
    print("\n[6] PFC 상태")
    state = pfc.get_state()
    print(f"  작업 기억: {state['working_memory_count']}/{state['working_memory_capacity']}")
    print(f"  현재 목표: {state['current_goal']}")

    print("\n" + "=" * 60)
    print("✅ PFC Engine 테스트 완료")
    print("=" * 60)


if __name__ == "__main__":
    main()
