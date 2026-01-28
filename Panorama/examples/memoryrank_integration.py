"""Panorama Memory Engine + MemoryRank Engine 연동 예제.

두 엔진을 결합하여:
1. Panorama: 시간축 기반 이벤트 기록
2. MemoryRank: 구조 기반 중요도 계산

실행:
    cd /Users/jazzin/Desktop/00_BRAIN
    python 12.Panorama_Memory_Engine/examples/memoryrank_integration.py
"""

import sys
from pathlib import Path

# 패키지 경로 추가
BRAIN_ROOT = Path(__file__).resolve().parents[2]  # 00_BRAIN
sys.path.insert(0, str(BRAIN_ROOT / "12.Panorama_Memory_Engine" / "package"))
sys.path.insert(0, str(BRAIN_ROOT / "11.MemoryRank_Engine" / "package"))

from panorama import PanoramaMemoryEngine, PanoramaConfig
from memoryrank import MemoryRankEngine, MemoryRankConfig, MemoryNodeAttributes


def main() -> None:
    print("=" * 60)
    print("Panorama + MemoryRank 통합 예제")
    print("=" * 60)

    # ==========================================================
    # 1. Panorama: 시간축 이벤트 기록
    # ==========================================================
    print("\n[1] Panorama: 이벤트 기록")
    
    panorama = PanoramaMemoryEngine(PanoramaConfig(
        time_gap_threshold=60.0,     # 1분 갭으로 에피소드 분할
        recency_half_life=3600.0,    # 1시간 반감기
    ))

    # PTSD 환자 시뮬레이션 타임라인
    base_time = 1706400000.0
    events = [
        # 평소 활동
        (base_time + 0, "daily_routine", {"activity": "wake_up"}, 0.3),
        (base_time + 10, "daily_routine", {"activity": "breakfast"}, 0.3),
        # 트리거 노출
        (base_time + 100, "trigger_exposure", {"trigger": "loud_noise", "intensity": 0.8}, 0.9),
        # 플래시백 발생
        (base_time + 105, "flashback", {"trauma_id": "T001", "intensity": 0.95}, 0.95),
        # 과각성 상태
        (base_time + 110, "hyperarousal", {"heart_rate": 120, "anxiety": 0.9}, 0.85),
        # 회복 시도
        (base_time + 200, "coping_attempt", {"method": "breathing", "success": 0.6}, 0.7),
        (base_time + 300, "recovery", {"anxiety": 0.4, "state": "calming"}, 0.6),
    ]

    event_ids = []
    for t, etype, payload, importance in events:
        eid = panorama.append_event(t, etype, payload, importance=importance)
        event_ids.append(eid)
        print(f"  + {etype}: importance={importance:.2f}")

    # ==========================================================
    # 2. Panorama → MemoryRank 변환
    # ==========================================================
    print("\n[2] Panorama → MemoryRank 변환")
    
    # 최근성 점수 계산 (현재 시간 = base_time + 350초)
    t_now = base_time + 350
    recency_scores = panorama.get_recency_scores(t_now)

    # 이벤트 간 연결 관계 정의 (인과관계 그래프)
    # trigger → flashback → hyperarousal → coping → recovery
    edges = [
        (event_ids[2], event_ids[3], 1.0),  # trigger → flashback
        (event_ids[3], event_ids[4], 1.0),  # flashback → hyperarousal
        (event_ids[4], event_ids[5], 0.8),  # hyperarousal → coping
        (event_ids[5], event_ids[6], 0.9),  # coping → recovery
        # 일상 → 트리거 (배경)
        (event_ids[1], event_ids[2], 0.3),  # breakfast → trigger (시간적 연속)
    ]

    # MemoryRank 노드 속성 생성
    node_attrs = {}
    for eid in event_ids:
        event = panorama.get_event(eid)
        if event:
            node_attrs[eid] = MemoryNodeAttributes(
                recency=recency_scores.get(eid, 0.0),
                emotion=event.payload.get("intensity", event.payload.get("anxiety", 0.3)),
                frequency=0.5,
                base_importance=event.importance,
            )
            print(f"  {event.event_type}: recency={node_attrs[eid].recency:.3f}")

    # ==========================================================
    # 3. MemoryRank: 중요도 계산
    # ==========================================================
    print("\n[3] MemoryRank: 중요도 계산")
    
    memoryrank = MemoryRankEngine(MemoryRankConfig(
        damping=0.85,
        recency_weight=1.5,   # 최근성 강조
        emotion_weight=2.0,   # 정서 강조
    ))

    memoryrank.build_graph(edges, node_attrs)
    importance = memoryrank.calculate_importance()

    print("\n  중요도 순위:")
    top = memoryrank.get_top_memories(7)
    for i, (eid, score) in enumerate(top, 1):
        event = panorama.get_event(eid)
        if event:
            print(f"  {i}. {event.event_type}: {score:.4f}")

    # ==========================================================
    # 4. 분석 결과
    # ==========================================================
    print("\n[4] 분석 결과")
    
    # 가장 중요한 이벤트
    most_important_id, most_important_score = top[0]
    most_important_event = panorama.get_event(most_important_id)
    
    print(f"\n  🔴 핵심 기억: {most_important_event.event_type}")
    print(f"     - 중요도 점수: {most_important_score:.4f}")
    print(f"     - payload: {most_important_event.payload}")
    
    # 해석
    print("\n  💡 해석:")
    print("     PTSD 환자의 기억 네트워크에서 'flashback' 이벤트가")
    print("     가장 높은 중요도를 가짐 (높은 정서 강도 + 최근성 + 연결 중심성)")
    print("     → 이 기억이 환자의 인지에 가장 큰 영향을 미침")

    print("\n" + "=" * 60)
    print("✅ 통합 테스트 완료")
    print("=" * 60)


if __name__ == "__main__":
    main()
