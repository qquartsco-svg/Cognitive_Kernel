"""PTSD-style flashback demo for MemoryRankEngine.

This example constructs a small trauma-related memory graph and ranks
memories by their importance, using higher emotion/recency for trauma nodes.

Run with:

    python 11.MemoryRank_Engine/examples/ptsd_flashback_demo.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "package"))

from memoryrank import MemoryRankEngine, MemoryRankConfig, MemoryNodeAttributes


def main() -> None:
    # 노드: 외상 장면, 병원 냄새, 사이렌 소리, 평범한 일상, 안전한 장소 등
    edges = [
        ("trauma_scene", "hospital_smell", 0.9),
        ("trauma_scene", "siren_sound", 0.8),
        ("hospital_smell", "panic_attack", 0.7),
        ("siren_sound", "panic_attack", 0.6),
        ("everyday_scene", "safe_place", 0.5),
        ("safe_place", "everyday_scene", 0.5),
    ]

    node_attrs = {
        # 외상 관련 기억: 최근성, 정서, 빈도 모두 높게
        "trauma_scene": MemoryNodeAttributes(recency=0.9, emotion=1.0, frequency=0.8),
        "hospital_smell": MemoryNodeAttributes(recency=0.8, emotion=0.9, frequency=0.7),
        "siren_sound": MemoryNodeAttributes(recency=0.7, emotion=0.9, frequency=0.6),
        "panic_attack": MemoryNodeAttributes(recency=0.8, emotion=1.0, frequency=0.7),
        # 중립/안전 기억: 정서 강도 낮고 빈도는 중간
        "everyday_scene": MemoryNodeAttributes(recency=0.5, emotion=0.2, frequency=0.5),
        "safe_place": MemoryNodeAttributes(recency=0.6, emotion=0.3, frequency=0.4),
    }

    cfg = MemoryRankConfig(damping=0.85, emotion_weight=1.5, recency_weight=1.0, frequency_weight=1.0)
    engine = MemoryRankEngine(cfg)
    engine.build_graph(edges, node_attrs)

    scores = engine.calculate_importance()

    print("[PTSD flashback-style MemoryRank scores]")
    for nid, score in sorted(scores.items(), key=lambda x: -x[1]):
        print(f"  {nid:15s}: {score:.4f}")

    print("\n[Top 3 intrusive memories]")
    for nid, score in engine.get_top_memories(3):
        print(f"  {nid:15s}: {score:.4f}")


if __name__ == "__main__":
    main()
