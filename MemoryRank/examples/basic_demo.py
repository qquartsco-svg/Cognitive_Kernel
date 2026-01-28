"""Basic demo for MemoryRankEngine.

Run with:

    python 11.MemoryRank_Engine/examples/basic_demo.py

This script builds a small toy memory graph and prints scores and top-k nodes.
"""

import sys
from pathlib import Path

# Add MemoryRank package to path
ROOT = Path(__file__).resolve().parents[1]  # 11.MemoryRank_Engine
sys.path.insert(0, str(ROOT / "package"))

from memoryrank import MemoryRankEngine, MemoryRankConfig, MemoryNodeAttributes


def main() -> None:
    edges = [
        ("memory_a", "memory_b", 1.0),
        ("memory_b", "memory_c", 1.0),
        ("memory_c", "memory_a", 0.5),
        ("memory_c", "memory_d", 0.8),
        ("memory_d", "memory_c", 0.2),
    ]

    node_attrs = {
        "memory_a": MemoryNodeAttributes(recency=0.3, emotion=0.4, frequency=0.5),
        "memory_b": MemoryNodeAttributes(recency=0.5, emotion=0.5, frequency=0.5),
        "memory_c": MemoryNodeAttributes(recency=0.9, emotion=0.9, frequency=0.9),
        "memory_d": MemoryNodeAttributes(recency=0.2, emotion=0.2, frequency=0.2),
    }

    engine = MemoryRankEngine(MemoryRankConfig())
    engine.build_graph(edges, node_attrs)

    scores = engine.calculate_importance()
    print("[MemoryRank scores]")
    for nid, score in sorted(scores.items(), key=lambda x: -x[1]):
        print(f"  {nid}: {score:.4f}")

    print("\n[Top 2 memories]")
    for nid, score in engine.get_top_memories(2):
        print(f"  {nid}: {score:.4f}")


if __name__ == "__main__":
    main()
