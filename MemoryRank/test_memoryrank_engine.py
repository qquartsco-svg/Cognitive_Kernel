import sys
from pathlib import Path

# MemoryRank 패키지 경로 추가
root = Path(__file__).resolve().parent  # 11.MemoryRank_Engine
sys.path.insert(0, str(root / "package"))

from memoryrank import MemoryRankEngine, MemoryRankConfig, MemoryNodeAttributes


def main() -> None:
    # 간단한 테스트 그래프
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

    engine = MemoryRankEngine(MemoryRankConfig(damping=0.85))
    engine.build_graph(edges, node_attrs)

    scores = engine.calculate_importance()
    print("Scores:")
    for k, v in sorted(scores.items()):
        print(f"  {k}: {v:.4f}")

    print("\nTop 3:")
    for nid, score in engine.get_top_memories(3):
        print(f"  {nid}: {score:.4f}")


if __name__ == "__main__":
    main()
