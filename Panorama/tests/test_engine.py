"""Panorama Memory Engine pytest 테스트."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "package"))

from panorama import PanoramaMemoryEngine, PanoramaConfig, Event


def test_append_and_query():
    """이벤트 추가 및 구간 쿼리 테스트."""
    engine = PanoramaMemoryEngine()
    
    base = 1000.0
    engine.append_event(base + 0, "a", {})
    engine.append_event(base + 5, "b", {})
    engine.append_event(base + 10, "c", {})
    
    assert len(engine) == 3
    
    # 구간 쿼리
    results = engine.query_range(base + 2, base + 8)
    assert len(results) == 1
    assert results[0].event_type == "b"


def test_episode_segmentation():
    """에피소드 자동 분할 테스트."""
    config = PanoramaConfig(time_gap_threshold=10.0)
    engine = PanoramaMemoryEngine(config)
    
    base = 1000.0
    # Episode 1: 0, 5
    engine.append_event(base + 0, "e1_a", {})
    engine.append_event(base + 5, "e1_b", {})
    # Gap: 20초 → 새 에피소드
    # Episode 2: 25, 30
    engine.append_event(base + 25, "e2_a", {})
    engine.append_event(base + 30, "e2_b", {})
    
    episodes = engine.segment_episodes(method="time_gap")
    assert len(episodes) == 2
    assert len(episodes[0].event_ids) == 2
    assert len(episodes[1].event_ids) == 2


def test_recent_events():
    """최근 이벤트 조회 테스트."""
    engine = PanoramaMemoryEngine()
    
    for i in range(10):
        engine.append_event(float(i), f"event_{i}", {})
    
    recent = engine.get_recent(3)
    assert len(recent) == 3
    assert recent[-1].event_type == "event_9"


def test_importance_scores():
    """중요도 점수 계산 테스트."""
    config = PanoramaConfig(recency_half_life=100.0)
    engine = PanoramaMemoryEngine(config)
    
    base = 1000.0
    eid1 = engine.append_event(base + 0, "old", {}, importance=1.0)
    eid2 = engine.append_event(base + 100, "new", {}, importance=1.0)
    
    t_now = base + 100
    scores = engine.get_importance_scores(t_now)
    
    # 100초 경과 = 반감기 → old의 중요도는 약 0.5
    assert scores[eid1] < scores[eid2]
    assert 0.45 < scores[eid1] < 0.55  # 약 0.5


def test_event_immutability():
    """Event 불변성 테스트."""
    engine = PanoramaMemoryEngine()
    eid = engine.append_event(1000.0, "test", {"key": "value"})
    event = engine.get_event(eid)
    
    # frozen=True이므로 수정 시도시 에러
    try:
        event.timestamp = 2000.0
        assert False, "Should raise FrozenInstanceError"
    except AttributeError:
        pass  # 예상대로 에러 발생


if __name__ == "__main__":
    test_append_and_query()
    test_episode_segmentation()
    test_recent_events()
    test_importance_scores()
    test_event_immutability()
    print("✅ All tests passed!")
