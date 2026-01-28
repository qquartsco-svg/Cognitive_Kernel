"""Panorama Memory Engine 테스트 스크립트.

실행:
    cd /Users/jazzin/Desktop/00_BRAIN
    python 12.Panorama_Memory_Engine/test_panorama_engine.py
"""

import sys
from pathlib import Path

# 패키지 경로 추가
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "package"))

from panorama import PanoramaMemoryEngine, PanoramaConfig


def main() -> None:
    print("=" * 60)
    print("Panorama Memory Engine v1.0 - Test")
    print("=" * 60)

    # 1. 엔진 초기화
    config = PanoramaConfig(time_gap_threshold=10.0)  # 10초 갭으로 에피소드 분할
    engine = PanoramaMemoryEngine(config)

    # 2. 이벤트 추가 (시뮬레이션된 타임라인)
    base_time = 1706400000.0  # 2024-01-28 00:00:00 UTC 근처

    events_data = [
        (base_time + 0, "session_start", {"user": "alice"}),
        (base_time + 2, "action", {"type": "click", "target": "button_a"}),
        (base_time + 5, "action", {"type": "scroll", "direction": "down"}),
        (base_time + 8, "state_change", {"state": "loading"}),
        # 15초 갭 → 새 에피소드
        (base_time + 25, "session_start", {"user": "alice"}),
        (base_time + 27, "action", {"type": "click", "target": "button_b"}),
        (base_time + 30, "memory_recall", {"memory_id": "trauma_001", "emotion": 0.9}),
        # 20초 갭 → 새 에피소드
        (base_time + 55, "session_end", {"user": "alice"}),
    ]

    print("\n[1] 이벤트 추가")
    for t, event_type, payload in events_data:
        eid = engine.append_event(t, event_type, payload, importance=0.5)
        print(f"  + {event_type} at t={t - base_time:.0f}s → {eid[:8]}...")

    print(f"\n총 이벤트 수: {len(engine)}")

    # 3. 시간 구간 쿼리
    print("\n[2] 구간 쿼리: t=0~10초")
    results = engine.query_range(base_time + 0, base_time + 10)
    for e in results:
        print(f"  - {e.event_type} at t={e.timestamp - base_time:.0f}s")

    # 4. 최근 이벤트
    print("\n[3] 최근 3개 이벤트")
    recent = engine.get_recent(3)
    for e in recent:
        print(f"  - {e.event_type} at t={e.timestamp - base_time:.0f}s")

    # 5. 에피소드 자동 분할
    print("\n[4] 에피소드 자동 분할 (time_gap=10초)")
    episodes = engine.segment_episodes(method="time_gap")
    for i, ep in enumerate(episodes):
        duration = (ep.end_time - ep.start_time) if ep.start_time and ep.end_time else 0
        print(f"  Episode {i+1}: {len(ep.event_ids)} events, duration={duration:.0f}s")

    # 6. 중요도 점수 (지수 감쇠)
    print("\n[5] 중요도 점수 (현재 시간 기준 지수 감쇠)")
    # 시뮬레이션: "현재"를 base_time + 60초로 설정
    t_now = base_time + 60
    scores = engine.get_importance_scores(t_now)
    sorted_scores = sorted(scores.items(), key=lambda x: -x[1])[:5]
    for eid, score in sorted_scores:
        event = engine.get_event(eid)
        if event:
            print(f"  {event.event_type}: {score:.4f}")

    print("\n" + "=" * 60)
    print("✅ 테스트 완료")
    print("=" * 60)


if __name__ == "__main__":
    main()
