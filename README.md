# Cognitive Kernel

> **🇰🇷 한국어** | [🇺🇸 English](#english-version)

> 기억, 주의력, 감정의 동역학을 탐구하기 위한 **모듈형 인지 프레임워크**

---

### 🎯 왜 지금 필요한가?

**현대 LLM 에이전트에는 구조화된 장기 기억과 실행 제어 기능이 부족합니다.**  
Cognitive Kernel은 이 갭을 메우기 위한 **drop-in 인지 서브시스템**을 제공합니다.

---

## 🧠 이것은 무엇인가?

**Cognitive Kernel**은 인지 기능을 모듈화한 **확장 가능한 프레임워크**입니다.

```
⚠️ 연구 및 실험 도구입니다.
   실제 뇌의 완전한 모델이 아니며, 임상 진단 도구가 아닙니다.
```

---

## ⭐ 핵심 기능

### 💾 진짜 장기 기억 (Persistence Layer)

v1.1.0부터 **영속성 레이어**가 추가되었습니다:

```python
# 저장 - 프로세스 종료 후에도 기억 유지
engine.save_to_json("memory.json")
engine.save_to_sqlite("memory.db")

# 로드 - 다른 세션에서 복구
engine.load_from_json("memory.json")
```

**이제 "장기 기억"이라는 표현이 정확합니다:**
- ✅ 프로세스 종료 후에도 기억 유지
- ✅ 파일/DB로 영구 보존
- ✅ 다른 세션에서 복구 가능

### 💡 MemoryRank — 중요도 기반 기억 랭킹

Google PageRank 알고리즘을 기억 네트워크에 적용:

```python
from memoryrank import MemoryRankEngine
engine = MemoryRankEngine()
engine.build_graph(edges, attributes)  # recency, emotion, frequency
top_memories = engine.get_top_memories(k=5)

# 장기 저장
engine.save_to_json("memory_graph.json")
```

### 🎬 PFC — 작업 기억 & 의사결정

Miller's Law (7±2) 기반 작업 기억과 Softmax 행동 선택:

```python
from pfc import PFCEngine, Action
pfc = PFCEngine()
pfc.load_from_memoryrank(top_memories)
action = pfc.select_action([Action(name="respond", expected_reward=0.8)])
```

---

## 🔧 활용 방향

### 🔬 연구용 (Research)

- 인지 모델 시뮬레이션
- 기억-감정-의사결정 동역학 연구
- 뇌 질환 메커니즘 탐구 (PTSD, ADHD 등)

### 🏭 산업용 (Industrial)

- AI 에이전트 메모리 서브시스템
- RAG 검색 결과 필터링/랭킹
- 추천 시스템 백본
- LangChain/LlamaIndex 통합

### 💼 상업용 (Commercial)

- 개인화된 AI 비서의 기억 레이어
- 게임 NPC 행동 엔진
- 교육용 시뮬레이터

---

## 🔗 설계 철학

### Edge AI First

모든 모듈은 **Edge 디바이스에서도 실행 가능**하도록 설계:

```
✅ 경량화된 알고리즘
✅ NumPy 외 필수 의존성 최소화
✅ 모듈별 독립 실행 가능
✅ 클라우드 의존성 없음
```

### 확장 가능한 구조

각 모듈은 **독립적**입니다. 필요한 것만 선택하세요:

```python
# 1개만 사용
from memoryrank import MemoryRankEngine

# 조합해서 사용
from memoryrank import MemoryRankEngine
from pfc import PFCEngine
from panorama import PanoramaMemoryEngine

# 직접 확장
class MyCustomEngine:
    def __init__(self):
        self.memory = MemoryRankEngine()
        self.decision = PFCEngine()
```

**사용자 확장 예시**:
- 새 엔진 추가 (Hippocampus, Cerebellum 등)
- 기존 엔진 커스터마이징
- 다른 프레임워크와 통합

---

## 📦 전체 모듈 구성

| 모듈 | 역할 | 핵심 알고리즘 | 영속성 |
|------|------|-------------|--------|
| **[MemoryRank](./MemoryRank/)** | 기억 중요도 | PageRank | ✅ JSON/NPZ |
| **[PFC](./PFC/)** | 의사결정 | Softmax Utility | |
| **[Panorama](./Panorama/)** | 시간축 기억 | Exponential Decay | ✅ JSON/SQLite |
| **[BasalGanglia](./BasalGanglia/)** | 습관 학습 | TD-Learning | |
| **[Amygdala](./Amygdala/)** | 감정/위협 | Rescorla-Wagner | |
| **[Hypothalamus](./Hypothalamus/)** | 에너지/상태 | HPA Dynamics | |
| **[Thalamus](./Thalamus/)** | 입력 필터링 | Salience Gating | |

---

## 💡 핵심 사용법 (3줄로 시작)

```python
from cognitive_kernel import CognitiveKernel

# 자동 저장/로드 세션
with CognitiveKernel("my_brain") as kernel:
    kernel.remember("meeting", {"topic": "project"}, importance=0.9)
    memories = kernel.recall(k=5)
    decision = kernel.decide(["rest", "work", "exercise"])
```

**이것만으로:**
- ✅ 기억 저장 (장기 기억)
- ✅ 중요도 계산 (PageRank)
- ✅ 의사결정 (Softmax)
- ✅ 자동 저장/복구

---

## 🚀 Quick Start

```bash
git clone https://github.com/qquartsco-svg/Cognitive_Kernel.git
cd Cognitive_Kernel
pip install numpy

# 개별 모듈 테스트
python MemoryRank/test_memoryrank_engine.py
python PFC/test_pfc_engine.py

# 통합 시뮬레이션
python examples/full_brain_simulation.py
```

---

## 📚 문서

| 문서 | 설명 |
|------|------|
| [ARCHITECTURE.md](./docs/ARCHITECTURE.md) | 이론적 기반, 수식, 참고 문헌 |
| [VERIFICATION_STATUS.md](./docs/VERIFICATION_STATUS.md) | 이론 ↔ 코드 일치 검증 |
| [ROADMAP.md](./docs/ROADMAP.md) | 구현 계획 |

---

## 🔐 PHAM Blockchain Signature

모든 핵심 모듈은 **PHAM (Proof of Honest Authorship & Merit)** 블록체인으로 서명:

| 모듈 | 서명 | 상세 |
|------|------|------|
| MemoryRank | ✅ | [서명](./MemoryRank/PHAM_BLOCKCHAIN_SIGNATURE.md) |
| Panorama | ✅ | [서명](./Panorama/PHAM_BLOCKCHAIN_SIGNATURE.md) |
| PFC | ✅ | [서명](./PFC/PHAM_BLOCKCHAIN_SIGNATURE.md) |
| BasalGanglia | ✅ | [서명](./BasalGanglia/BLOCKCHAIN_INFO.md) |
| Amygdala | ✅ | [서명](./Amygdala/BLOCKCHAIN_INFO.md) |
| Hypothalamus | ✅ | [서명](./Hypothalamus/BLOCKCHAIN_INFO.md) |
| Thalamus | ✅ | [서명](./Thalamus/BLOCKCHAIN_INFO.md) |

---

## 📄 License

MIT License — 자유롭게 사용, 수정, 배포 가능

---

## 👤 Author

**GNJz (Qquarts)** — [@qquartsco-svg](https://github.com/qquartsco-svg)

---

---

# English Version

> [🇰🇷 한국어](#cognitive-kernel) | **🇺🇸 English**

> A **modular cognitive framework** for exploring dynamics of memory, attention, and emotion

---

### 🎯 Why Now?

**Modern LLM agents lack structured long-term memory and executive control.**  
Cognitive Kernel provides **drop-in cognitive subsystems** to address this gap.

---

## 🧠 What is this?

**Cognitive Kernel** is an **extensible framework** with modularized cognitive functions.

```
⚠️ Research and experimentation tool.
   NOT a complete model of the brain, nor a clinical diagnostic tool.
```

---

## ⭐ Core Features

### 💾 True Long-term Memory (Persistence Layer)

v1.1.0 adds **persistence layer**:

```python
# Save - memory persists after process termination
engine.save_to_json("memory.json")
engine.save_to_sqlite("memory.db")

# Load - recover in different session
engine.load_from_json("memory.json")
```

**"Long-term memory" is now accurate:**
- ✅ Memory persists after process termination
- ✅ Permanent storage in file/DB
- ✅ Recoverable in different sessions

### 💡 MemoryRank — Importance-based Memory Ranking

Applies Google's PageRank algorithm to memory networks:

```python
from memoryrank import MemoryRankEngine
engine = MemoryRankEngine()
engine.build_graph(edges, attributes)  # recency, emotion, frequency
top_memories = engine.get_top_memories(k=5)

# Long-term storage
engine.save_to_json("memory_graph.json")
```

### 🎬 PFC — Working Memory & Decision Making

Miller's Law (7±2) working memory and Softmax action selection:

```python
from pfc import PFCEngine, Action
pfc = PFCEngine()
pfc.load_from_memoryrank(top_memories)
action = pfc.select_action([Action(name="respond", expected_reward=0.8)])
```

---

## 🔧 Use Cases

### 🔬 Research

- Cognitive model simulation
- Memory-emotion-decision dynamics research
- Brain disorder mechanism exploration (PTSD, ADHD, etc.)

### 🏭 Industrial

- AI agent memory subsystem
- RAG result filtering/ranking
- Recommendation system backbone
- LangChain/LlamaIndex integration

### 💼 Commercial

- Personalized AI assistant memory layer
- Game NPC behavior engine
- Educational simulators

---

## 🔗 Design Philosophy

### Edge AI First

All modules designed to **run on Edge devices**:

```
✅ Lightweight algorithms
✅ Minimal dependencies (NumPy only)
✅ Each module runs independently
✅ No cloud dependency
```

### Extensible Structure

Each module is **independent**. Use only what you need:

```python
# Use one
from memoryrank import MemoryRankEngine

# Combine
from memoryrank import MemoryRankEngine
from pfc import PFCEngine
from panorama import PanoramaMemoryEngine

# Extend yourself
class MyCustomEngine:
    def __init__(self):
        self.memory = MemoryRankEngine()
        self.decision = PFCEngine()
```

**User extension examples**:
- Add new engines (Hippocampus, Cerebellum, etc.)
- Customize existing engines
- Integrate with other frameworks

---

## 📦 All Modules

| Module | Role | Core Algorithm | Persistence |
|--------|------|---------------|-------------|
| **[MemoryRank](./MemoryRank/)** | Memory importance | PageRank | ✅ JSON/NPZ |
| **[PFC](./PFC/)** | Decision making | Softmax Utility | |
| **[Panorama](./Panorama/)** | Timeline memory | Exponential Decay | ✅ JSON/SQLite |
| **[BasalGanglia](./BasalGanglia/)** | Habit learning | TD-Learning | |
| **[Amygdala](./Amygdala/)** | Emotion/Threat | Rescorla-Wagner | |
| **[Hypothalamus](./Hypothalamus/)** | Energy/State | HPA Dynamics | |
| **[Thalamus](./Thalamus/)** | Input filtering | Salience Gating | |

---

## 💡 핵심 사용법 (3줄로 시작)

```python
from cognitive_kernel import CognitiveKernel

# 자동 저장/로드 세션
with CognitiveKernel("my_brain") as kernel:
    kernel.remember("meeting", {"topic": "project"}, importance=0.9)
    memories = kernel.recall(k=5)
    decision = kernel.decide(["rest", "work", "exercise"])
```

**이것만으로:**
- ✅ 기억 저장 (장기 기억)
- ✅ 중요도 계산 (PageRank)
- ✅ 의사결정 (Softmax)
- ✅ 자동 저장/복구

---

## 🚀 Quick Start

```bash
git clone https://github.com/qquartsco-svg/Cognitive_Kernel.git
cd Cognitive_Kernel
pip install numpy

# Test individual modules
python MemoryRank/test_memoryrank_engine.py
python PFC/test_pfc_engine.py

# Full simulation
python examples/full_brain_simulation.py
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](./docs/ARCHITECTURE.md) | Theoretical foundation, formulas, references |
| [VERIFICATION_STATUS.md](./docs/VERIFICATION_STATUS.md) | Theory ↔ Code verification |
| [ROADMAP.md](./docs/ROADMAP.md) | Implementation plan |

---

## 🔐 PHAM Blockchain Signature

All core modules signed with **PHAM (Proof of Honest Authorship & Merit)** blockchain:

| Module | Signed | Details |
|--------|--------|---------|
| MemoryRank | ✅ | [Signature](./MemoryRank/PHAM_BLOCKCHAIN_SIGNATURE.md) |
| Panorama | ✅ | [Signature](./Panorama/PHAM_BLOCKCHAIN_SIGNATURE.md) |
| PFC | ✅ | [Signature](./PFC/PHAM_BLOCKCHAIN_SIGNATURE.md) |
| BasalGanglia | ✅ | [Signature](./BasalGanglia/BLOCKCHAIN_INFO.md) |
| Amygdala | ✅ | [Signature](./Amygdala/BLOCKCHAIN_INFO.md) |
| Hypothalamus | ✅ | [Signature](./Hypothalamus/BLOCKCHAIN_INFO.md) |
| Thalamus | ✅ | [Signature](./Thalamus/BLOCKCHAIN_INFO.md) |

---

## 📄 License

MIT License — Free to use, modify, and distribute

---

## 👤 Author

**GNJz (Qquarts)** — [@qquartsco-svg](https://github.com/qquartsco-svg)

---

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a Pull Request.
