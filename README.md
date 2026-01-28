# Cognitive Kernel

> **🇰🇷 한국어** | [🇺🇸 English](#english-version)

> 기억, 주의력, 감정의 동역학을 탐구하기 위한 **모듈형 인지 프레임워크**

**현대 LLM 에이전트에는 구조화된 장기 기억과 실행 제어 기능이 부족합니다.**  
**Cognitive Kernel은 이 갭을 메우기 위한 drop-in 인지 서브시스템을 제공합니다.**

---

## 🧠 이것은 무엇인가?

**Cognitive Kernel**은 인지 기능을 모듈화한 **확장 가능한 프레임워크**입니다.

각 모듈은 독립적으로 사용하거나, 조합하여 더 복잡한 시스템을 구축할 수 있습니다.

```
⚠️ 이 프레임워크는 연구 및 실험 도구입니다.
   실제 뇌의 완전한 모델이 아니며, 임상 진단 도구가 아닙니다.
   모든 결과는 추가 검증이 필요합니다.
```

---

## ⭐ 핵심 모듈

### 💡 MemoryRank — 중요도 기반 기억 랭킹

Google PageRank 알고리즘을 기억 네트워크에 적용한 모듈입니다.

```python
from memoryrank import MemoryRankEngine
engine = MemoryRankEngine()
engine.build_graph(edges, attributes)  # recency, emotion, frequency
top_memories = engine.get_top_memories(k=5)
```

**활용 가능 방향**: RAG 검색 결과 필터링, AI 에이전트 장기 기억, 추천 시스템

→ [MemoryRank 상세](./MemoryRank/)

---

### 🎬 PFC — 작업 기억 & 의사결정

Miller's Law (7±2) 기반 작업 기억과 Softmax 행동 선택을 구현한 모듈입니다.

```python
from pfc import PFCEngine, Action
pfc = PFCEngine()
pfc.load_from_memoryrank(top_memories)
action = pfc.select_action([Action(name="respond", expected_reward=0.8)])
```

**활용 가능 방향**: AI 에이전트 의사결정, 멀티스텝 추론, 행동 억제

→ [PFC 상세](./PFC/)

---

### 📦 전체 모듈 구성

| 모듈 | 역할 | 핵심 알고리즘 | 상세 |
|------|------|-------------|------|
| **[MemoryRank](./MemoryRank/)** | 기억 중요도 | PageRank | ⭐ 권장 |
| **[PFC](./PFC/)** | 의사결정 | Softmax Utility | ⭐ 권장 |
| **[Panorama](./Panorama/)** | 시간축 기억 | Exponential Decay | |
| **[BasalGanglia](./BasalGanglia/)** | 습관 학습 | TD-Learning | |
| **[Amygdala](./Amygdala/)** | 감정/위협 | Rescorla-Wagner | |
| **[Hypothalamus](./Hypothalamus/)** | 에너지/상태 | HPA Dynamics | |
| **[Thalamus](./Thalamus/)** | 입력 필터링 | Salience Gating | |

---

## 🔗 확장 가능한 구조

각 모듈은 **독립적**입니다. 필요한 것만 선택해서 사용하세요.

```python
# 1개만 사용
from memoryrank import MemoryRankEngine

# 조합해서 사용
from memoryrank import MemoryRankEngine
from pfc import PFCEngine

# 전체 파이프라인
from examples.full_brain_simulation import CognitiveKernel
```

**사용자 확장 예시**:
- 새로운 엔진 추가 (Hippocampus, Cerebellum 등)
- 기존 엔진 커스터마이징 (Config 파라미터 조정)
- 다른 시스템과 통합 (LangChain, LlamaIndex 등)

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

모든 핵심 모듈은 **PHAM (Proof of Honest Authorship & Merit)** 블록체인으로 서명되어 있습니다.

| 모듈 | 서명 | 상세 |
|------|------|------|
| MemoryRank | ✅ | [서명 문서](./MemoryRank/PHAM_BLOCKCHAIN_SIGNATURE.md) |
| Panorama | ✅ | [서명 문서](./Panorama/PHAM_BLOCKCHAIN_SIGNATURE.md) |
| PFC | ✅ | [서명 문서](./PFC/PHAM_BLOCKCHAIN_SIGNATURE.md) |
| BasalGanglia | ✅ | [서명 문서](./BasalGanglia/BLOCKCHAIN_INFO.md) |
| Amygdala | ✅ | [서명 문서](./Amygdala/BLOCKCHAIN_INFO.md) |
| Hypothalamus | ✅ | [서명 문서](./Hypothalamus/BLOCKCHAIN_INFO.md) |
| Thalamus | ✅ | [서명 문서](./Thalamus/BLOCKCHAIN_INFO.md) |

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

**Modern LLM agents lack structured long-term memory and executive control.**  
**Cognitive Kernel provides drop-in cognitive subsystems to address this gap.**

---

## 🧠 What is this?

**Cognitive Kernel** is an **extensible framework** with modularized cognitive functions.

Each module can be used independently or combined to build more complex systems.

```
⚠️ This framework is a research and experimentation tool.
   It is NOT a complete model of the actual brain, nor a clinical diagnostic tool.
   All results require further validation.
```

---

## ⭐ Core Modules

### 💡 MemoryRank — Importance-based Memory Ranking

Applies Google's PageRank algorithm to memory networks.

```python
from memoryrank import MemoryRankEngine
engine = MemoryRankEngine()
engine.build_graph(edges, attributes)  # recency, emotion, frequency
top_memories = engine.get_top_memories(k=5)
```

**Potential directions**: RAG result filtering, AI agent long-term memory, recommendation systems

→ [MemoryRank Details](./MemoryRank/)

---

### 🎬 PFC — Working Memory & Decision Making

Implements Miller's Law (7±2) working memory and Softmax action selection.

```python
from pfc import PFCEngine, Action
pfc = PFCEngine()
pfc.load_from_memoryrank(top_memories)
action = pfc.select_action([Action(name="respond", expected_reward=0.8)])
```

**Potential directions**: AI agent decision-making, multi-step reasoning, action inhibition

→ [PFC Details](./PFC/)

---

### 📦 All Modules

| Module | Role | Core Algorithm | Details |
|--------|------|---------------|---------|
| **[MemoryRank](./MemoryRank/)** | Memory importance | PageRank | ⭐ Recommended |
| **[PFC](./PFC/)** | Decision making | Softmax Utility | ⭐ Recommended |
| **[Panorama](./Panorama/)** | Timeline memory | Exponential Decay | |
| **[BasalGanglia](./BasalGanglia/)** | Habit learning | TD-Learning | |
| **[Amygdala](./Amygdala/)** | Emotion/Threat | Rescorla-Wagner | |
| **[Hypothalamus](./Hypothalamus/)** | Energy/State | HPA Dynamics | |
| **[Thalamus](./Thalamus/)** | Input filtering | Salience Gating | |

---

## 🔗 Extensible Structure

Each module is **independent**. Use only what you need.

```python
# Use one
from memoryrank import MemoryRankEngine

# Combine
from memoryrank import MemoryRankEngine
from pfc import PFCEngine

# Full pipeline
from examples.full_brain_simulation import CognitiveKernel
```

**User extension examples**:
- Add new engines (Hippocampus, Cerebellum, etc.)
- Customize existing engines (adjust Config parameters)
- Integrate with other systems (LangChain, LlamaIndex, etc.)

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

All core modules are signed with **PHAM (Proof of Honest Authorship & Merit)** blockchain.

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
