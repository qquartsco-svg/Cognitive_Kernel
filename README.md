# 🧠 Cognitive Kernel

> **Give your AI agent persistent memory. 3 lines of code.**  
> **AI 에이전트에게 영구 기억을 부여하세요. 3줄의 코드로.**

[![PyPI version](https://badge.fury.io/py/cognitive-kernel.svg)](https://pypi.org/project/cognitive-kernel/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Cognitive Kernel**은 뇌와 유사한 기억, 의사결정, 인지 동역학을 시뮬레이션하는 모듈형 인지 프레임워크입니다.

> **🇰🇷 한국어** (기본) | [🇺🇸 English Version](#english-version)

---

## 🎯 Cognitive Kernel이란?

**Cognitive Kernel**은 AI 에이전트에게 **영구 기억(Persistent Memory)**과 **인지 동역학(Cognitive Dynamics)**을 제공하는 프레임워크입니다.

### 핵심 개념

기존 AI 시스템의 문제점:
- ❌ 프로세스 종료 시 기억 소실
- ❌ 정적 확률 분포 (동적 피드백 없음)
- ❌ 불안정한 의사결정

**Cognitive Kernel**의 해결책:
- ✅ **영구 기억**: 프로세스 종료 후에도 기억 유지
- ✅ **동적 피드백**: 엔트로피 기반 자동 탐색
- ✅ **안정적 의사결정**: 메모리 중력(코어 강도) 기반 수렴

### 수학 구조 해석 엔진

`Cognitive_Kernel`은 이제 단순 기억 커널을 넘어,
브레인 수학 엔진 축의 최종 해석기를 포함합니다.

| 엔진 | 역할 |
|------|------|
| `irrational_algebra` | 상태 벡터의 무리수 공명, 대수적 불변식, 경계/관측/동역학 건강도를 결합한 구조 해석 |

이 엔진은 `ENGINE_HUB` 쪽 수학 엔진들과 다음 관계를 가집니다.

```text
AlgebraApprox_Engine         → 근사 방법론
IrrationalApprox_Engine     → 무리수 수렴 생성
ConvergenceDynamics_Engine  → 수렴 과정 판정
irrational_algebra          → 구조 해석
```

즉 `Cognitive_Kernel`은 수렴을 만드는 곳이 아니라,
현재 상태의 구조적 질서를 읽는 **수학 해석 코어**입니다.

---

## 🚀 빠른 시작

```python
from cognitive_kernel import CognitiveKernel

# 커널 생성
kernel = CognitiveKernel()

# 기억 저장
kernel.remember("I like coffee", importance=0.9)

# 의사결정
decision = kernel.decide(["rest", "work", "exercise"])
print(decision["action"])  # "work"
```

---

## 🧠 핵심 기능

### 7개 핵심 엔진

| 엔진 | 역할 | 핵심 알고리즘 |
|------|------|-------------|
| **Panorama Memory** | 시간축 이벤트 저장 | 지수 감쇠 (Ebbinghaus) |
| **MemoryRank** | 기억 중요도 랭킹 | Personalized PageRank |
| **Prefrontal Cortex (PFC)** | 의사결정 | Softmax Utility |
| **Basal Ganglia** | 습관 형성 | Q-Learning |
| **Thalamus** | 입력 필터링 | Salience Gating |
| **Amygdala** | 감정 처리 | Rescorla-Wagner |
| **Hypothalamus** | 에너지 관리 | HPA Dynamics |

### 인지 동역학 (Cognitive Dynamics)

**Cognitive Kernel**은 단순한 확률 계산을 넘어 **인지 상태의 물리적 동역학**을 모델링합니다:

#### 1. 엔트로피 기반 동역학 (Entropy-based Dynamics)

**엔트로피**는 선택의 불확실성을 측정합니다:

```
E = -Σ P(k) ln P(k)
```

- **높은 엔트로피**: 불확실한 선택 (탐색 필요)
- **낮은 엔트로피**: 확정적인 선택 (착취)

**자동 회전 토크 생성**:
```
T(k) = γ * E_norm * cos(φ - ψ_k)
```

엔트로피가 높을수록 더 강한 회전 토크가 생성되어 자동으로 탐색을 유도합니다.

#### 2. 코어 강도 (Core Strength)

**코어 강도**는 기억의 중력입니다. 엔트로피를 다시 수렴시키는 힘:

```
C(t) = C(0) * exp(-λ * Δt)
```

- **높은 코어 강도**: 강한 기억, 엔트로피를 수렴시킬 수 있음
- **낮은 코어 강도**: 약한 기억, 엔트로피가 퍼짐 (치매/알츠하이머)

#### 3. 세차운동 (Precession)

선택 분포가 상태 공간에서 **느리게 회전**하는 현상:

- 엔트로피 기반 토크가 생성
- 위상이 느리게 업데이트: `φ(t+1) = φ(t) + ω`
- 탐색-착취 균형을 자동으로 조절

#### 4. Maxwell 구조 (Maxwell Structure)

**ADHD(+)와 ASD(-) 극**이 인지 상태 공간에 **유효 자기장**을 생성합니다:

- **ADHD**: 높은 엔트로피 → 강한 회전 → 탐색
- **ASD**: 낮은 엔트로피 → 약한 회전 → 착취

→ [상세 설명: Maxwell Structure](docs/MAXWELL_STRUCTURE.md)

#### 5. 코어 붕괴 (Core Decay)

**치매/알츠하이머 모델링**:

**치매 (Dementia)**:
- 오래된 기억 감쇠: `importance *= exp(-λ_old * age)`
- 새 기억은 정상 유지
- 코어 강도 점진적 감소

**알츠하이머 (Alzheimer's)**:
- 새 기억 즉시 감쇠: `importance *= exp(-λ_new * age)`
- 코어 강도 급격한 붕괴
- 메모리 업데이트 실패율 높음

→ [상세 설명: Dementia & Alzheimer's](docs/DEMENTIA_ALZHEIMER_IMPLEMENTATION.md)

---

## 🎯 인지 모드 (Cognitive Modes)

**Cognitive Kernel**은 다양한 인지 상태를 시뮬레이션할 수 있습니다:

### 기본 모드
- `NORMAL`: 정상 상태
- `ADHD`: 높은 엔트로피, 강한 회전 (과도한 탐색)
- `ASD`: 낮은 엔트로피, 약한 회전 (과도한 착취)
- `PTSD`: 트라우마 고착

### 고급 모드
- `PANIC`: 엔트로피 폭주
- `EPILEPSY`: 급격한 상태 전환
- `OCD`: 루프 고착
- `IED`: 순간 토크 스파이크
- `DEPRESSION`: 저엔트로피 + 저코어
- `BIPOLAR`: 상태 간 자동 전이

### 붕괴 모드 ⭐
- `DEMENTIA`: 코어 강도 점진적 감소 (오래된 기억부터 소실)
- `ALZHEIMER`: 코어 강도 급격한 붕괴 (새 기억 저장 실패)

```python
# 모드 설정
kernel.set_mode("ADHD")      # 높은 엔트로피, 강한 회전
kernel.set_mode("ASD")       # 낮은 엔트로피, 약한 회전
kernel.set_mode("DEMENTIA")  # 코어 강도 점진적 감소
kernel.set_mode("ALZHEIMER") # 코어 강도 급격한 붕괴
```

---

## 📦 설치

```bash
pip install cognitive-kernel
```

---

## 💡 사용 예시

### 기본 기억 & 의사결정

```python
from cognitive_kernel import CognitiveKernel

kernel = CognitiveKernel()

# 기억 저장
kernel.remember("I prefer morning coffee", importance=0.9)
kernel.remember("I exercise at 6pm", importance=0.8)

# 의사결정
decision = kernel.decide(["rest", "work", "exercise"])
print(decision["action"])  # "exercise"
print(decision["probability_distribution"])
# {'rest': 0.2, 'work': 0.3, 'exercise': 0.5}
```

### 인지 모드 사용

```python
# ADHD 모드 (높은 엔트로피, 강한 회전)
kernel.set_mode("ADHD")
decision = kernel.decide(["rest", "work", "exercise"])
# 더 다양한 선택 분포 (탐색 강화)

# ASD 모드 (낮은 엔트로피, 약한 회전)
kernel.set_mode("ASD")
decision = kernel.decide(["rest", "work", "exercise"])
# 더 집중된 선택 분포 (착취 강화)

# 치매 모드 (코어 강도 감소)
kernel.set_mode("DEMENTIA")
# 오래된 기억부터 소실, 새 기억은 정상
```

### 장기 기억 (Long-term Memory)

```python
# 세션 저장
kernel.save_session("my_session.json")

# 다음 프로세스에서 세션 로드
kernel = CognitiveKernel()
kernel.load_session("my_session.json")

# 기억이 복구됨!
memories = kernel.recall(k=5)
print(f"복구된 기억: {len(memories)}개")
```

---

## 🏗️ 아키텍처

```
Cognitive Kernel
├── Panorama Memory      (이벤트 저장)
├── MemoryRank           (중요도 랭킹)
├── Prefrontal Cortex    (의사결정)
├── Basal Ganglia        (습관 형성)
├── Thalamus             (입력 필터링)
├── Amygdala             (감정 처리)
├── Hypothalamus         (에너지 관리)
└── Dynamics Engine      (엔트로피, 코어, 토크)
```

---

## 📚 문서

### 핵심 개념
- [Maxwell Structure in State Space](docs/MAXWELL_STRUCTURE.md) - ADHD/ASD 극과 자기장
- [Physical Dynamics](docs/PHYSICAL_DYNAMICS.md) - 세차운동과 회전 동역학
- [Stability Core](docs/STABILITY_CORE.md) - 정신적 회복력 모델

### 고급 기능
- [Dementia & Alzheimer's Dynamics](docs/DEMENTIA_ALZHEIMER_IMPLEMENTATION.md) - 기억 상실 모델링
- [Dynamics Engine](docs/DYNAMICS_ENGINE_FUNCTIONS.md) - 엔트로피, 코어 강도, 토크
- [Disorder Spectrum](docs/DISORDER_SPECTRUM_ANALYSIS.md) - 인지 장애 매핑

### 기술 문서
- [API Reference](docs/API_REFERENCE.md)
- [Version History](docs/version_history/VERSION_HISTORY.md)
- [PHAM Blockchain](docs/version_history/PHAM_BLOCKCHAIN_LOG.md)

---

## 🔬 인지 동역학 상세 설명

### 엔트로피 & 코어 강도

**엔트로피**는 선택의 불확실성을 측정합니다:

```
E = -Σ P(k) ln P(k)
```

**코어 강도**는 기억의 중력으로, 엔트로피를 다시 수렴시킵니다:

```
C(t) = C(0) * exp(-λ * Δt)
```

### 세차운동 & 회전 토크

시스템은 엔트로피를 기반으로 **자동 회전 토크**를 생성합니다:

```
T(k) = γ * E_norm * cos(φ - ψ_k)
```

이것은 상태 공간에서 선호 축의 **세차운동(느린 회전)**을 생성합니다.

### Maxwell 구조

**ADHD(+)와 ASD(-) 극**이 인지 상태 공간에 **유효 자기장**을 생성합니다:

- **ADHD**: 높은 엔트로피 → 강한 회전 → 탐색
- **ASD**: 낮은 엔트로피 → 약한 회전 → 착취

→ [상세 설명: Maxwell Structure](docs/MAXWELL_STRUCTURE.md)

### 치매 & 알츠하이머

**치매**: 코어 강도 점진적 감소
- 오래된 기억 감쇠율 높음 (`old_memory_decay_rate`)
- 새 기억은 정상 유지

**알츠하이머**: 코어 강도 급격한 붕괴
- 새 기억 즉시 감쇠 (`new_memory_decay_rate`)
- 코어 감쇠율 높음
- 메모리 업데이트 실패

→ [상세 설명: Dementia & Alzheimer's](docs/DEMENTIA_ALZHEIMER_IMPLEMENTATION.md)

---

## 🔗 관련 프로젝트

- [Dynamics Engine](https://github.com/qquartsco-svg/Dynamic_engine) - 독립 동역학 모듈
- [MemoryRank Engine](https://github.com/qquartsco-svg/MemoryRank_Engine) - 기억 중요도 랭킹

---

## 📄 라이선스

MIT License

---

## 👤 작성자

**GNJz (Qquarts)**

---

---

# English Version

> **🇰🇷 [한국어 버전](#-cognitive-kernel이란) (기본)** | **🇺🇸 English**

## 🎯 What is Cognitive Kernel?

**Cognitive Kernel** is a modular cognitive framework that simulates brain-like memory, decision-making, and cognitive dynamics for AI agents.

### Core Concept

Problems with existing AI systems:
- ❌ Memory loss on process termination
- ❌ Static probability distributions (no dynamic feedback)
- ❌ Unstable decision-making

**Cognitive Kernel** solution:
- ✅ **Persistent Memory**: Memory survives process termination
- ✅ **Dynamic Feedback**: Entropy-based automatic exploration
- ✅ **Stable Decision-making**: Memory gravity (core strength) based convergence

---

## 🚀 Quick Start

```python
from cognitive_kernel import CognitiveKernel

# Create kernel
kernel = CognitiveKernel()

# Remember
kernel.remember("I like coffee", importance=0.9)

# Decide
decision = kernel.decide(["rest", "work", "exercise"])
print(decision["action"])  # "work"
```

---

## 🧠 Core Features

### 7 Core Engines

| Engine | Role | Core Algorithm |
|--------|------|---------------|
| **Panorama Memory** | Temporal event storage | Exponential Decay (Ebbinghaus) |
| **MemoryRank** | Memory importance ranking | Personalized PageRank |
| **Prefrontal Cortex (PFC)** | Decision-making | Softmax Utility |
| **Basal Ganglia** | Habit formation | Q-Learning |
| **Thalamus** | Input filtering | Salience Gating |
| **Amygdala** | Emotion processing | Rescorla-Wagner |
| **Hypothalamus** | Energy management | HPA Dynamics |

### Cognitive Dynamics

**Cognitive Kernel** models the **physics of cognitive states**, not just probability calculations:

#### 1. Entropy-based Dynamics

**Entropy** measures choice uncertainty:

```
E = -Σ P(k) ln P(k)
```

- **High entropy**: Uncertain choices (exploration needed)
- **Low entropy**: Certain choices (exploitation)

**Automatic rotational torque generation**:
```
T(k) = γ * E_norm * cos(φ - ψ_k)
```

Higher entropy generates stronger rotational torque, automatically inducing exploration.

#### 2. Core Strength

**Core Strength** is memory gravity that reconverges entropy:

```
C(t) = C(0) * exp(-λ * Δt)
```

- **High core strength**: Strong memory, can reconverge entropy
- **Low core strength**: Weak memory, entropy spreads (dementia/Alzheimer's)

#### 3. Precession

Slow rotation of choice distribution in state space:

- Entropy-based torque is generated
- Phase slowly updates: `φ(t+1) = φ(t) + ω`
- Automatically balances exploration-exploitation

#### 4. Maxwell Structure

**ADHD(+) and ASD(-) poles** create an **effective magnetic field** in cognitive state space:

- **ADHD**: High entropy → Strong rotation → Exploration
- **ASD**: Low entropy → Weak rotation → Exploitation

→ [Details: Maxwell Structure](docs/MAXWELL_STRUCTURE.md)

#### 5. Core Decay

**Dementia/Alzheimer's modeling**:

**Dementia**:
- Old memory decay: `importance *= exp(-λ_old * age)`
- New memories remain intact
- Gradual core strength decrease

**Alzheimer's**:
- New memory immediate decay: `importance *= exp(-λ_new * age)`
- Rapid core strength collapse
- High memory update failure rate

→ [Details: Dementia & Alzheimer's](docs/DEMENTIA_ALZHEIMER_IMPLEMENTATION.md)

---

## 🎯 Cognitive Modes

**Cognitive Kernel** can simulate various cognitive states:

### Basic Modes
- `NORMAL`: Normal state
- `ADHD`: High entropy, strong rotation (over-exploration)
- `ASD`: Low entropy, weak rotation (over-exploitation)
- `PTSD`: Trauma fixation

### Advanced Modes
- `PANIC`: Entropy explosion
- `EPILEPSY`: Rapid state transition
- `OCD`: Loop fixation
- `IED`: Instantaneous torque spike
- `DEPRESSION`: Low entropy + low core
- `BIPOLAR`: Automatic state transition

### Collapse Modes ⭐
- `DEMENTIA`: Gradual core strength decrease (old memories lost first)
- `ALZHEIMER`: Rapid core strength collapse (new memory storage failure)

```python
# Set mode
kernel.set_mode("ADHD")      # High entropy, strong rotation
kernel.set_mode("ASD")       # Low entropy, weak rotation
kernel.set_mode("DEMENTIA")  # Gradual core strength decrease
kernel.set_mode("ALZHEIMER") # Rapid core strength collapse
```

---

## 📦 Installation

```bash
pip install cognitive-kernel
```

---

## 💡 Usage Examples

### Basic Memory & Decision

```python
from cognitive_kernel import CognitiveKernel

kernel = CognitiveKernel()

# Remember events
kernel.remember("I prefer morning coffee", importance=0.9)
kernel.remember("I exercise at 6pm", importance=0.8)

# Decide
decision = kernel.decide(["rest", "work", "exercise"])
print(decision["action"])  # "exercise"
```

### Cognitive Modes

```python
# ADHD mode (high entropy, strong rotation)
kernel.set_mode("ADHD")

# ASD mode (low entropy, weak rotation)
kernel.set_mode("ASD")

# Dementia mode (core decay)
kernel.set_mode("DEMENTIA")

# Alzheimer's mode (rapid core collapse)
kernel.set_mode("ALZHEIMER")
```

### Long-term Memory

```python
# Save session
kernel.save_session("my_session.json")

# Load session
kernel.load_session("my_session.json")
```

---

## 🏗️ Architecture

```
Cognitive Kernel
├── Panorama Memory (Event Storage)
├── MemoryRank (Importance Ranking)
├── Prefrontal Cortex (Decision-making)
├── Basal Ganglia (Habit Formation)
├── Thalamus (Input Filtering)
├── Amygdala (Emotion Processing)
├── Hypothalamus (Energy Management)
└── Dynamics Engine (Entropy, Core, Torque)
```

---

## 📚 Documentation

### Core Concepts
- [Maxwell Structure in State Space](docs/MAXWELL_STRUCTURE.md) - ADHD/ASD poles and magnetic field
- [Physical Dynamics](docs/PHYSICAL_DYNAMICS.md) - Precession and rotational dynamics
- [Stability Core](docs/STABILITY_CORE.md) - Mental resilience model

### Advanced Features
- [Dementia & Alzheimer's Dynamics](docs/DEMENTIA_ALZHEIMER_IMPLEMENTATION.md) - Memory loss modeling
- [Dynamics Engine](docs/DYNAMICS_ENGINE_FUNCTIONS.md) - Entropy, core strength, torque
- [Disorder Spectrum](docs/DISORDER_SPECTRUM_ANALYSIS.md) - Cognitive disorder mapping

### Technical
- [API Reference](docs/API_REFERENCE.md)
- [Version History](docs/version_history/VERSION_HISTORY.md)
- [PHAM Blockchain](docs/version_history/PHAM_BLOCKCHAIN_LOG.md)

---

## 🔗 Related Projects

- [Dynamics Engine](https://github.com/qquartsco-svg/Dynamic_engine) - Standalone dynamics module
- [MemoryRank Engine](https://github.com/qquartsco-svg/MemoryRank_Engine) - Memory ranking

---

## 📄 License

MIT License

---

## 👤 Author

**GNJz (Qquarts)**

---

**Version**: 2.0.2  
**Last Updated**: 2026-01-31
