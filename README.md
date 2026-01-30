# 🧠 Cognitive Kernel

[![PyPI version](https://badge.fury.io/py/cognitive-kernel.svg)](https://pypi.org/project/cognitive-kernel/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **🇰🇷 한국어** | [🇺🇸 English](#english-version)

## **Give your AI agent persistent memory. 3 lines of code.**

기억의 시간 인코딩, 중요도 랭킹, 의사결정 반영을 결합한 모듈형 인지 프레임워크.

---

## 📦 Installation

```bash
pip install cognitive-kernel
```

---

## ⚡ Why Hybrid Memory Matters (Real Example)

**시나리오**: 과거에 낮은 중요도로 저장된 선호도가, 수많은 기억들 사이에 묻혔다가, **Hybrid Cognitive Kernel에 의해 다시 회상되어 실제 의사결정을 바꾸는 순간**

### ❌ Vector DB Only Result:

```
Query: 'schedule a meeting'
Found 5 results:

1. [related_event] Distance: 0.712
   Text: Had to reschedule morning meeting to afternoon...
2. [related_event] Distance: 0.772
   Text: Team agreed afternoon meetings work better...
3. [preference] Distance: 0.903 ⚠️  (Original preference)
   Text: I hate morning meetings. They make me unproductive.
```

**→ Preference가 3위, 관련 이벤트들이 위에 있음**

### ✅ Hybrid (Vector DB + Cognitive Kernel) Result:

```
Query: 'schedule a meeting'
Found 4 hybrid-ranked results:

1. [preference] Hybrid Score: 0.251 ⚠️  (Original preference)
   Importance: 0.478, Vector Distance: 0.903
   Text: I hate morning meetings. They make me unproductive.
2. [related_event] Hybrid Score: 0.102
   Importance: 0.174, Vector Distance: 0.712
   Text: Had to reschedule morning meeting to afternoon...
```

**→ Preference가 1위로 REVIVED!**  
**→ Decision: Schedule afternoon meeting (CORRECT!)**

### 📊 Comparison:

| Metric | Vector Only | Hybrid Kernel |
|--------|-------------|---------------|
| Preference in Top 3 | ✅ (3위) | ✅ (1위) |
| Importance Re-ranking | ❌ | ✅ (PageRank) |
| Correct Decision | ⚠️ | ✅ |

**💡 Key Insight**: Vector DB는 semantic similarity만 보지만, Cognitive Kernel은 **연결 관계를 통해 importance를 재계산**하여 묻힌 선호도를 되살립니다.

→ [Full Example](./examples/hybrid_failure_vs_success.py)

---

## 🔗 LangChain Integration (NEW!)

```python
from cognitive_kernel import CognitiveKernel

# Your LLM agent now has persistent, ranked memory
with CognitiveKernel("my_agent") as memory:
    memory.remember("user_preference", {"likes": "morning meetings"})
    
    # Next day (new process) - agent still remembers!
    recalled = memory.recall(k=5)  # PageRank-ranked memories
```

**Before vs After:**

| Feature | Standard Memory | Cognitive Kernel |
|---------|----------------|------------------|
| Persistence | ❌ Lost on restart | ✅ Survives forever |
| Importance | ❌ FIFO buffer | ✅ PageRank ranking |
| Time Decay | ❌ None | ✅ Ebbinghaus curve |

→ [Full LangChain Example](./examples/langchain_memory.py)

---

## 🔗 Vector DB Integration (NEW!)

**의미 기억(Semantic Memory)을 Vector DB에 저장하고, Cognitive Kernel로 중요도 재랭킹**

```python
from cognitive_kernel import CognitiveKernel, VectorDBBackend

# Vector DB 백엔드 초기화
vector_backend = VectorDBBackend(
    backend_type="chroma",
    path="./chroma_db",
    collection_name="cognitive_memory"
)

# Cognitive Kernel과 함께 사용
kernel = CognitiveKernel("my_agent")

# 기억 저장 (Vector DB + Cognitive Kernel)
memory_id = kernel.remember("preference", {"text": "I like coffee"})
vector_backend.add_memory(memory_id, "I like coffee", metadata={})

# Semantic Search (Vector DB)
results = vector_backend.search("coffee preference", k=5)

# Importance Ranking (MemoryRank)
ranked = kernel.recall(k=5)  # PageRank-based
```

**하이브리드 검색 구조:**

```
[Embedding Model] → [Vector DB (Chroma/FAISS)]  ← Semantic Search
                            ↓
                    [MemoryRank]                  ← Importance Re-ranking
                            ↓
                    [PFC]                         ← Decision Making
```

**Before vs After:**

| Feature | Vector DB Only | Vector DB + Cognitive Kernel |
|---------|----------------|------------------------------|
| Semantic Search | ✅ | ✅ |
| Importance Ranking | ❌ | ✅ (PageRank) |
| Time Decay | ❌ | ✅ (Ebbinghaus) |
| Hybrid Search | ❌ | ✅ (Combined) |

→ [Full Vector DB Example](./examples/vector_db_chroma.py)

**설치:**
```bash
pip install cognitive-kernel chromadb sentence-transformers
# 또는
pip install cognitive-kernel[vector]
```

---

## 🎯 왜 지금 필요한가?

**현대 LLM 에이전트에는 구조화된 장기 기억과 실행 제어 기능이 부족합니다.**

Cognitive Kernel은 이 갭을 메우기 위한 **drop-in 인지 서브시스템**을 제공합니다.

```
⚠️ 연구 및 실험 도구입니다.
   실제 뇌의 완전한 모델이 아니며, 임상 진단 도구가 아닙니다.

📌 This project does not claim biological equivalence to human memory.
   It provides a computer-science definition of long-term memory:
   persistent, structured, recallable, and decision-impacting.
```

---

## ⭐ 핵심 기능: 3줄로 시작하는 장기 기억

```python
from cognitive_kernel import CognitiveKernel

with CognitiveKernel("my_brain") as kernel:
    kernel.remember("meeting", {"topic": "project"}, importance=0.9)
    memories = kernel.recall(k=5)           # PageRank 기반 중요도 회상
    decision = kernel.decide(["rest", "work"])  # Softmax 의사결정
# 자동 저장됨 → 프로세스 종료 후에도 기억 유지
```

### ✅ 이것만으로:

| 기능 | 설명 | 알고리즘 |
|------|------|----------|
| `remember()` | 기억 저장 (장기 기억) | 시간축 저장 + 자동 영속성 |
| `recall()` | 중요한 기억 회상 | **Google PageRank** |
| `decide()` | 의사결정 | **Softmax Utility** |

→ [장기 기억 상세 설명](./docs/LONG_TERM_MEMORY.md)

---

## 📐 핵심 수식

### 1. 기억 중요도 (MemoryRank)

**Personalized PageRank** 알고리즘:

$$
\mathbf{r}^{(t+1)} = \alpha \cdot M \cdot \mathbf{r}^{(t)} + (1-\alpha) \cdot \mathbf{v}
$$

- $\mathbf{r}$: 기억 중요도 벡터
- $M$: 기억 전이 행렬 (열 정규화)
- $\alpha$: 감쇠 계수 (기본값: 0.85)
- $\mathbf{v}$: 개인화 벡터 (recency, emotion, frequency 가중치)

### 2. 시간 감쇠 (Panorama)

**지수 감쇠 함수**:

$$
S(t) = S_0 \cdot e^{-\lambda \cdot \Delta t}, \quad \lambda = \frac{\ln 2}{t_{1/2}}
$$

- $S(t)$: 시간 $t$에서의 중요도
- $t_{1/2}$: 반감기 (기본값: 3600초 = 1시간)

### 3. 의사결정 (PFC)

**Softmax 선택 확률**:

$$
P(a_i) = \frac{e^{U(a_i) / T}}{\sum_j e^{U(a_j) / T}}
$$

- $U(a)$: 행동 $a$의 효용 = 기대보상 - 비용 - 위험
- $T$: 온도 (탐색 vs 착취 균형)

→ [이론적 기반 상세](./docs/ARCHITECTURE.md)

---

## 💾 장기 기억이란?

### 컴퓨터 공학적 정의

> **영속성(Persistence)**: 프로세스 종료 후에도 데이터가 유지됨

### Cognitive Kernel의 구현

```
세션 A (프로세스 1)          세션 B (프로세스 2)
─────────────────────      ─────────────────────
kernel.remember(...)  →    파일 저장
        ↓                       ↓
프로세스 종료              CognitiveKernel("my_brain")
                                ↓
                           자동 로드 → 기억 복구!
```

### 저장 구조

```
.cognitive_kernel/my_brain/
├── panorama.json      # 시간축 이벤트 (기억 데이터)
├── memoryrank.json    # 중요도 그래프
├── edges.json         # 기억 연결 관계
├── q_values.json      # 습관 학습 (Q-Learning)
└── meta.json          # 세션 메타데이터
```

→ [장기 기억 기술 문서](./docs/LONG_TERM_MEMORY.md)

---

## 🧪 테스트 결과

### 장기 기억 증명

```bash
# 테스트 실행
cd /Users/jazzin/Desktop/00_BRAIN/Cognitive_Kernel
python3 cognitive_kernel.py
```

**결과:**

```
📦 Session: test_session
📝 기억 저장... 3개
🔍 기억 회상 (Top 3): idea(0.349), conversation(0.333), meeting(0.318)
🎯 의사결정: rest (효용: 0.250)
✅ 자동 저장 완료!

🔄 세션 복구 테스트...
   복구된 이벤트: 3개 ← 프로세스 종료 후에도 유지됨!
```

### 7개 엔진 통합 시뮬레이션

| 시나리오 | Stress Max | Hyperarousal | Efficiency | Alerts |
|---------|-----------|--------------|------------|--------|
| Normal Day | 0.44 | 1회 | 0.71 | 1개 |
| PTSD | **0.80** | **3회** | **0.61** | **5개** |

→ [전체 테스트 결과](./docs/TEST_RESULTS.md)

---

## 📦 전체 모듈 구성

| 모듈 | 역할 | 핵심 알고리즘 | 영속성 |
|------|------|-------------|--------|
| **[MemoryRank](./MemoryRank/)** | 기억 중요도 | PageRank | ✅ JSON/NPZ |
| **[Panorama](./Panorama/)** | 시간축 기억 | Exponential Decay | ✅ JSON/SQLite |
| **[PFC](./PFC/)** | 의사결정 | Softmax Utility | |
| **[BasalGanglia](./BasalGanglia/)** | 습관 학습 | TD-Learning | ✅ Q-values |
| **[Amygdala](./Amygdala/)** | 감정/위협 | Rescorla-Wagner | |
| **[Hypothalamus](./Hypothalamus/)** | 에너지/스트레스 | HPA Dynamics | |
| **[Thalamus](./Thalamus/)** | 입력 필터링 | Salience Gating | |

---

## 🔧 활용 방향

### 🔬 연구용 (Research)

- 인지 모델 시뮬레이션
- 기억-감정-의사결정 동역학 연구
- 뇌 질환 메커니즘 탐구 (PTSD, ADHD 등)

### 🏭 산업용 (Industrial)

- AI 에이전트 메모리 서브시스템
- RAG 검색 결과 필터링/랭킹
- LangChain/LlamaIndex 통합

### 💼 상업용 (Commercial)

- 개인화된 AI 비서의 기억 레이어
- 게임 NPC 행동 엔진
- 교육용 시뮬레이터

---

## 🔗 설계 철학

### Edge AI First

```
✅ 경량 알고리즘 (NumPy 외 필수 의존성 없음)
✅ 모듈별 독립 실행 가능
✅ 클라우드 의존성 없음
✅ 확장 가능한 구조
```

### 모듈 조합

```python
# 1개만 사용
from memoryrank import MemoryRankEngine

# 조합해서 사용
from cognitive_kernel import CognitiveKernel

# 직접 확장
class MyBrain(CognitiveKernel):
    def custom_recall(self): ...
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/qquartsco-svg/Cognitive_Kernel.git
cd Cognitive_Kernel
pip install numpy

# 장기 기억 테스트
python3 cognitive_kernel.py

# 7개 엔진 통합 시뮬레이션
python3 examples/full_brain_simulation.py

# 4개 핵심 파이프라인
python3 examples/integrated_pipeline.py
```

---

## 📚 문서

| 문서 | 설명 |
|------|------|
| [LONG_TERM_MEMORY.md](./docs/LONG_TERM_MEMORY.md) | 장기 기억 기술 문서 |
| [API_REFERENCE.md](./docs/API_REFERENCE.md) | API 레퍼런스 |
| [ARCHITECTURE.md](./docs/ARCHITECTURE.md) | 이론적 기반, 수식, 참고 문헌 |
| [TEST_RESULTS.md](./docs/TEST_RESULTS.md) | 전체 테스트 결과 |
| [VERIFICATION_STATUS.md](./docs/VERIFICATION_STATUS.md) | 이론 ↔ 코드 일치 검증 |

---

## 🔐 PHAM Blockchain Signature

모든 핵심 모듈은 **PHAM (Proof of Honest Authorship & Merit)** 블록체인으로 서명:

| 모듈 | 서명 | 등급 |
|------|------|------|
| cognitive_kernel.py | ✅ | A_HIGH (0.9998) |
| MemoryRank | ✅ | [서명](./MemoryRank/PHAM_BLOCKCHAIN_SIGNATURE.md) |
| Panorama | ✅ | [서명](./Panorama/PHAM_BLOCKCHAIN_SIGNATURE.md) |
| PFC | ✅ | [서명](./PFC/PHAM_BLOCKCHAIN_SIGNATURE.md) |

---

## 📄 License

MIT License — 자유롭게 사용, 수정, 배포 가능

---

## 👤 Author

**GNJz (Qquarts)** — [@qquartsco-svg](https://github.com/qquartsco-svg)

---

---

# English Version

> [🇰🇷 한국어](#-cognitive-kernel) | **🇺🇸 English**

## **Give your AI agent persistent memory. 3 lines of code.**

## 📦 Installation

```bash
pip install cognitive-kernel
```

---

## ⚡ Why Hybrid Memory Matters (Real Example)

**Scenario**: A preference stored with low importance gets buried among many memories, then **revived by Hybrid Cognitive Kernel to change actual decisions**

### ❌ Vector DB Only Result:

```
Query: 'schedule a meeting'
Found 5 results:

1. [related_event] Distance: 0.712
   Text: Had to reschedule morning meeting to afternoon...
2. [related_event] Distance: 0.772
   Text: Team agreed afternoon meetings work better...
3. [preference] Distance: 0.903 ⚠️  (Original preference)
   Text: I hate morning meetings. They make me unproductive.
```

**→ Preference ranked 3rd, related events above it**

### ✅ Hybrid (Vector DB + Cognitive Kernel) Result:

```
Query: 'schedule a meeting'
Found 4 hybrid-ranked results:

1. [preference] Hybrid Score: 0.251 ⚠️  (Original preference)
   Importance: 0.478, Vector Distance: 0.903
   Text: I hate morning meetings. They make me unproductive.
2. [related_event] Hybrid Score: 0.102
   Importance: 0.174, Vector Distance: 0.712
   Text: Had to reschedule morning meeting to afternoon...
```

**→ Preference REVIVED to 1st place!**  
**→ Decision: Schedule afternoon meeting (CORRECT!)**

### 📊 Comparison:

| Metric | Vector Only | Hybrid Kernel |
|--------|-------------|---------------|
| Preference in Top 3 | ✅ (3rd) | ✅ (1st) |
| Importance Re-ranking | ❌ | ✅ (PageRank) |
| Correct Decision | ⚠️ | ✅ |

**💡 Key Insight**: Vector DB only sees semantic similarity, but Cognitive Kernel **recalculates importance via connections** to revive buried preferences.

→ [Full Example](./examples/hybrid_failure_vs_success.py)

---

## 🔗 LangChain Integration (NEW!)

```python
from cognitive_kernel import CognitiveKernel

# Your LLM agent now has persistent, ranked memory
with CognitiveKernel("my_agent") as memory:
    memory.remember("user_preference", {"likes": "morning meetings"})
    
    # Next day (new process) - agent still remembers!
    recalled = memory.recall(k=5)  # PageRank-ranked memories
```

**Before vs After:**

| Feature | Standard Memory | Cognitive Kernel |
|---------|----------------|------------------|
| Persistence | ❌ Lost on restart | ✅ Survives forever |
| Importance | ❌ FIFO buffer | ✅ PageRank ranking |
| Time Decay | ❌ None | ✅ Ebbinghaus curve |

→ [Full LangChain Example](./examples/langchain_memory.py)

---

## 🔗 Vector DB Integration (NEW!)

**Store semantic memory in Vector DB, re-rank by Cognitive Kernel importance**

```python
from cognitive_kernel import CognitiveKernel, VectorDBBackend

# Initialize Vector DB backend
vector_backend = VectorDBBackend(
    backend_type="chroma",
    path="./chroma_db",
    collection_name="cognitive_memory"
)

# Use with Cognitive Kernel
kernel = CognitiveKernel("my_agent")

# Store memory (Vector DB + Cognitive Kernel)
memory_id = kernel.remember("preference", {"text": "I like coffee"})
vector_backend.add_memory(memory_id, "I like coffee", metadata={})

# Semantic Search (Vector DB)
results = vector_backend.search("coffee preference", k=5)

# Importance Ranking (MemoryRank)
ranked = kernel.recall(k=5)  # PageRank-based
```

**Hybrid Search Architecture:**

```
[Embedding Model] → [Vector DB (Chroma/FAISS)]  ← Semantic Search
                            ↓
                    [MemoryRank]                  ← Importance Re-ranking
                            ↓
                    [PFC]                         ← Decision Making
```

**Before vs After:**

| Feature | Vector DB Only | Vector DB + Cognitive Kernel |
|---------|----------------|------------------------------|
| Semantic Search | ✅ | ✅ |
| Importance Ranking | ❌ | ✅ (PageRank) |
| Time Decay | ❌ | ✅ (Ebbinghaus) |
| Hybrid Search | ❌ | ✅ (Combined) |

→ [Full Vector DB Example](./examples/vector_db_chroma.py)

**Installation:**
```bash
pip install cognitive-kernel chromadb sentence-transformers
# or
pip install cognitive-kernel[vector]
```

---

## 🎯 Why Now?

**Modern LLM agents lack structured long-term memory and executive control.**

Cognitive Kernel provides **drop-in cognitive subsystems** to address this gap.

```
⚠️ Research and experimentation tool.
   NOT a complete model of the brain, nor a clinical diagnostic tool.

📌 This project does not claim biological equivalence to human memory.
   It provides a computer-science definition of long-term memory:
   persistent, structured, recallable, and decision-impacting.
```

---

## ⭐ Core Feature: Long-term Memory in 3 Lines

```python
from cognitive_kernel import CognitiveKernel

with CognitiveKernel("my_brain") as kernel:
    kernel.remember("meeting", {"topic": "project"}, importance=0.9)
    memories = kernel.recall(k=5)           # PageRank-based importance recall
    decision = kernel.decide(["rest", "work"])  # Softmax decision-making
# Auto-saved → Memory persists after process termination
```

### ✅ This gives you:

| Feature | Description | Algorithm |
|---------|-------------|-----------|
| `remember()` | Store memory (long-term) | Timeline storage + auto-persistence |
| `recall()` | Recall important memories | **Google PageRank** |
| `decide()` | Decision making | **Softmax Utility** |

→ [Long-term Memory Details](./docs/LONG_TERM_MEMORY.md)

---

## 📐 Core Formulas

### 1. Memory Importance (MemoryRank)

**Personalized PageRank** algorithm:

$$
\mathbf{r}^{(t+1)} = \alpha \cdot M \cdot \mathbf{r}^{(t)} + (1-\alpha) \cdot \mathbf{v}
$$

- $\mathbf{r}$: Memory importance vector
- $M$: Memory transition matrix (column-normalized)
- $\alpha$: Damping factor (default: 0.85)
- $\mathbf{v}$: Personalization vector (recency, emotion, frequency weights)

### 2. Temporal Decay (Panorama)

**Exponential decay function**:

$$
S(t) = S_0 \cdot e^{-\lambda \cdot \Delta t}, \quad \lambda = \frac{\ln 2}{t_{1/2}}
$$

- $S(t)$: Importance at time $t$
- $t_{1/2}$: Half-life (default: 3600s = 1 hour)

### 3. Decision Making (PFC)

**Softmax selection probability**:

$$
P(a_i) = \frac{e^{U(a_i) / T}}{\sum_j e^{U(a_j) / T}}
$$

- $U(a)$: Utility of action $a$ = expected reward - cost - risk
- $T$: Temperature (exploration vs exploitation balance)

→ [Theoretical Foundation](./docs/ARCHITECTURE.md)

---

## 💾 What is Long-term Memory?

### Computer Science Definition

> **Persistence**: Data survives process termination

### Cognitive Kernel Implementation

```
Session A (Process 1)          Session B (Process 2)
─────────────────────         ─────────────────────
kernel.remember(...)  →       File saved
        ↓                          ↓
Process terminates            CognitiveKernel("my_brain")
                                   ↓
                              Auto-load → Memory recovered!
```

### Storage Structure

```
.cognitive_kernel/my_brain/
├── panorama.json      # Timeline events (memory data)
├── memoryrank.json    # Importance graph
├── edges.json         # Memory connections
├── q_values.json      # Habit learning (Q-Learning)
└── meta.json          # Session metadata
```

→ [Long-term Memory Technical Docs](./docs/LONG_TERM_MEMORY.md)

---

## 🧪 Test Results

### Long-term Memory Proof

```bash
# Run test
cd /Users/jazzin/Desktop/00_BRAIN/Cognitive_Kernel
python3 cognitive_kernel.py
```

**Result:**

```
📦 Session: test_session
📝 Memories saved: 3
🔍 Recall (Top 3): idea(0.349), conversation(0.333), meeting(0.318)
🎯 Decision: rest (utility: 0.250)
✅ Auto-saved!

🔄 Session recovery test...
   Recovered events: 3 ← Persists after process termination!
```

### 7-Engine Integration Simulation

| Scenario | Stress Max | Hyperarousal | Efficiency | Alerts |
|----------|-----------|--------------|------------|--------|
| Normal Day | 0.44 | 1 | 0.71 | 1 |
| PTSD | **0.80** | **3** | **0.61** | **5** |

→ [Full Test Results](./docs/TEST_RESULTS.md)

---

## 📦 All Modules

| Module | Role | Core Algorithm | Persistence |
|--------|------|---------------|-------------|
| **[MemoryRank](./MemoryRank/)** | Memory importance | PageRank | ✅ JSON/NPZ |
| **[Panorama](./Panorama/)** | Timeline memory | Exponential Decay | ✅ JSON/SQLite |
| **[PFC](./PFC/)** | Decision making | Softmax Utility | |
| **[BasalGanglia](./BasalGanglia/)** | Habit learning | TD-Learning | ✅ Q-values |
| **[Amygdala](./Amygdala/)** | Emotion/Threat | Rescorla-Wagner | |
| **[Hypothalamus](./Hypothalamus/)** | Energy/Stress | HPA Dynamics | |
| **[Thalamus](./Thalamus/)** | Input filtering | Salience Gating | |

---

## 🔧 Use Cases

### 🔬 Research

- Cognitive model simulation
- Memory-emotion-decision dynamics research
- Brain disorder mechanism exploration (PTSD, ADHD, etc.)

### 🏭 Industrial

- AI agent memory subsystem
- RAG result filtering/ranking
- LangChain/LlamaIndex integration

### 💼 Commercial

- Personalized AI assistant memory layer
- Game NPC behavior engine
- Educational simulators

---

## 🔗 Design Philosophy

### Edge AI First

```
✅ Lightweight algorithms (only NumPy dependency)
✅ Each module runs independently
✅ No cloud dependency
✅ Extensible structure
```

### Module Composition

```python
# Use one
from memoryrank import MemoryRankEngine

# Combine
from cognitive_kernel import CognitiveKernel

# Extend
class MyBrain(CognitiveKernel):
    def custom_recall(self): ...
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/qquartsco-svg/Cognitive_Kernel.git
cd Cognitive_Kernel
pip install numpy

# Long-term memory test
python3 cognitive_kernel.py

# 7-engine simulation
python3 examples/full_brain_simulation.py

# 4-engine pipeline
python3 examples/integrated_pipeline.py
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [LONG_TERM_MEMORY.md](./docs/LONG_TERM_MEMORY.md) | Long-term memory technical docs |
| [API_REFERENCE.md](./docs/API_REFERENCE.md) | API Reference |
| [ARCHITECTURE.md](./docs/ARCHITECTURE.md) | Theoretical foundation, formulas, references |
| [TEST_RESULTS.md](./docs/TEST_RESULTS.md) | Full test results |
| [VERIFICATION_STATUS.md](./docs/VERIFICATION_STATUS.md) | Theory ↔ Code verification |

---

## 🔐 PHAM Blockchain Signature

All core modules signed with **PHAM (Proof of Honest Authorship & Merit)** blockchain:

| Module | Signed | Grade |
|--------|--------|-------|
| cognitive_kernel.py | ✅ | A_HIGH (0.9998) |
| MemoryRank | ✅ | [Signature](./MemoryRank/PHAM_BLOCKCHAIN_SIGNATURE.md) |
| Panorama | ✅ | [Signature](./Panorama/PHAM_BLOCKCHAIN_SIGNATURE.md) |
| PFC | ✅ | [Signature](./PFC/PHAM_BLOCKCHAIN_SIGNATURE.md) |

---

## 📄 License

MIT License — Free to use, modify, and distribute

---

## 👤 Author

**GNJz (Qquarts)** — [@qquartsco-svg](https://github.com/qquartsco-svg)

---

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a Pull Request.
