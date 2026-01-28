"""Smoke test for MemoryRankEngine.

Run with:

    cd /Users/jazzin/Desktop/00_BRAIN
    python -m pytest 11.MemoryRank_Engine/tests
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "package"))

from memoryrank import MemoryRankEngine, MemoryRankConfig, MemoryNodeAttributes


def test_basic_ranking():
    edges = [
        ("A", "B", 1.0),
        ("B", "C", 1.0),
        ("C", "A", 1.0),
        ("C", "D", 0.5),
    ]

    node_attrs = {
        "A": MemoryNodeAttributes(recency=0.2, emotion=0.5, frequency=0.3),
        "B": MemoryNodeAttributes(recency=0.4, emotion=0.4, frequency=0.4),
        "C": MemoryNodeAttributes(recency=0.9, emotion=0.9, frequency=0.9),
        "D": MemoryNodeAttributes(recency=0.1, emotion=0.1, frequency=0.1),
    }

    engine = MemoryRankEngine(MemoryRankConfig())
    engine.build_graph(edges, node_attrs)
    scores = engine.calculate_importance()

    # 점수 합이 1에 가까운지 확인
    assert abs(sum(scores.values()) - 1.0) < 1e-6

    # C 가 가장 높은 점수를 가져야 함
    top = max(scores.items(), key=lambda x: x[1])[0]
    assert top == "C"
