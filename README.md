# Cognitive Kernel

> **인지 운영체제** — 기억, 주의력, 추론을 통합 관리하는 모듈형 인지 엔진

---

## 🧠 개요

**Cognitive Kernel**은 인간의 인지 시스템을 소프트웨어로 모델링한 **모듈형 인지 엔진 모음**입니다.

마치 운영체제의 커널이 CPU, 메모리, I/O를 관리하듯,
Cognitive Kernel은 **기억, 주의력, 감정, 추론**을 관리합니다.

---

## 🎬 기억의 영화관 비유

```
┌─────────────────────────────────────────────────────────────┐
│                    🧠 Cognitive Kernel                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   🎞️ Panorama (필름)                                        │
│   └─ 삶의 모든 순간을 시간순으로 기록                          │
│                         ↓                                   │
│   💡 MemoryRank (조광기)                                     │
│   └─ 수만 개 필름 중 어디에 조명을 비출지 결정                  │
│                         ↓                                   │
│   🎬 PFC (영사기 + 감독) [구현 예정]                           │
│   └─ 조명 비춰진 필름을 스크린에 투사, 다음 행동 결정            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 모듈 구성

| 모듈 | 역할 | 비유 | 상태 |
|------|------|------|------|
| **[MemoryRank](./MemoryRank/)** | 기억 중요도 계산 | 조광기 | ✅ v1.0.0 |
| **[Panorama](./Panorama/)** | 시간축 에피소드 기억 | 필름 | ✅ v1.0.0 |
| **[PFC](./PFC/)** | 작업 기억, 행동 선택, 억제 | 영사기 + 감독 | ✅ v1.0.0 |
| **[BasalGanglia](./BasalGanglia/)** | 행동 선택, 습관 학습, Q-Learning | 스태프 | ✅ v1.0.0 |

---

## 🔗 모듈 간 연결

```
┌──────────────┐     recency      ┌──────────────┐
│   Panorama   │ ───────────────▶ │  MemoryRank  │
│   (시간 기록) │                  │  (중요도 계산) │
└──────────────┘                  └──────────────┘
       │                                 │
       │ 이벤트 조회                      │ 상위 기억 추출
       ▼                                 ▼
┌──────────────────────────────────────────────┐
│                    PFC                        │
│         (추론 / 계획 / 의사결정)               │
└──────────────────────────────────────────────┘
```

### 데이터 흐름 예시

1. **Panorama**: 사용자 행동을 시간순으로 기록
2. **Panorama → MemoryRank**: 최근성(recency) 점수 전달
3. **MemoryRank**: 구조 + 정서 + 최근성 기반 중요도 계산
4. **MemoryRank → PFC**: 상위 N개 중요 기억 전달
5. **PFC**: 중요 기억 기반 추론 및 행동 결정

---

## 🚀 Quick Start

### 설치

\`\`\`bash
git clone https://github.com/qquartsco-svg/Cognitive_Kernel.git
cd Cognitive_Kernel
\`\`\`

### MemoryRank 사용

\`\`\`python
from MemoryRank.package.memoryrank import MemoryRankEngine, MemoryNodeAttributes

engine = MemoryRankEngine()
edges = [("A", "B", 1.0), ("B", "C", 1.0), ("C", "A", 0.5)]
node_attrs = {
    "A": MemoryNodeAttributes(recency=0.9, emotion=0.8),
    "B": MemoryNodeAttributes(recency=0.5, emotion=0.3),
    "C": MemoryNodeAttributes(recency=0.7, emotion=0.6),
}
engine.build_graph(edges, node_attrs)
top = engine.get_top_memories(3)
print(top)  # [('A', 0.42), ('C', 0.35), ('B', 0.23)]
\`\`\`

### Panorama 사용

\`\`\`python
from Panorama.package.panorama import PanoramaMemoryEngine

engine = PanoramaMemoryEngine()
import time
t = time.time()
engine.append_event(t, "click", {"target": "button"})
engine.append_event(t + 5, "scroll", {"direction": "down"})

# 구간 쿼리
events = engine.query_range(t, t + 10)

# 에피소드 분할
episodes = engine.segment_episodes()
\`\`\`

### 두 엔진 연동

\`\`\`python
from Panorama.package.panorama import PanoramaMemoryEngine
from MemoryRank.package.memoryrank import MemoryRankEngine, MemoryNodeAttributes

# Panorama에서 이벤트 기록
panorama = PanoramaMemoryEngine()
# ... (이벤트 추가)

# MemoryRank로 중요도 계산
recency_scores = panorama.get_recency_scores()
node_attrs = {
    eid: MemoryNodeAttributes(recency=recency_scores[eid])
    for eid in recency_scores
}

memoryrank = MemoryRankEngine()
memoryrank.build_graph(edges, node_attrs)
top_memories = memoryrank.get_top_memories(10)
\`\`\`

---

## 🎯 활용 분야

### 🏢 산업/상용

| 분야 | 활용 |
|------|------|
| **AI 에이전트** | 장기 기억 + 문맥 인식 대화 |
| **추천 시스템** | 사용자 관심사 중요도 기반 추천 |
| **게임 AI** | NPC 기억 시스템, 플레이어 행동 학습 |
| **로그 분석** | 인시던트 타임라인 재구성 |

### 🔬 연구/의료

| 분야 | 활용 |
|------|------|
| **PTSD 연구** | 외상 기억의 침입 패턴 분석 |
| **우울증 연구** | 부정적 기억 편향 시뮬레이션 |
| **ADHD 연구** | 주의력 붕괴 시점 추적 |
| **뇌 시뮬레이션** | 인지 루프 동역학 모델링 |

---

## 📁 프로젝트 구조

\`\`\`
Cognitive_Kernel/
├── README.md               # 이 파일 (통합 설명)
├── MemoryRank/             # 기억 중요도 계산 엔진
│   ├── README.md           # MemoryRank 개별 문서
│   ├── package/memoryrank/
│   ├── examples/
│   └── tests/
├── Panorama/               # 시간축 에피소드 기억 엔진
│   ├── README.md           # Panorama 개별 문서
│   ├── package/panorama/
│   ├── examples/
│   └── tests/
└── (향후 PFC, Basal_Ganglia 추가)
\`\`\`

---

## 🔬 이론적 배경

### OS Kernel vs Cognitive Kernel

| OS Kernel | Cognitive Kernel |
|-----------|------------------|
| Memory Manager | Panorama + MemoryRank |
| Process Scheduler | Attention Controller |
| System Call | 엔진 간 API |
| Kernel Panic | 인지 붕괴 (질환 상태) |

### 핵심 알고리즘

| 모듈 | 알고리즘 |
|------|----------|
| MemoryRank | Personalized PageRank |
| Panorama | Binary Search + Exponential Decay |
| PFC (예정) | Working Memory + Planning |

---

## 📄 License

MIT License

---

## 🔐 PHAM Blockchain Signature

모든 핵심 모듈은 **PHAM (Proof of Honest Authorship & Merit)** 블록체인 서명이 완료되어 있습니다.

| 모듈 | 서명 상태 |
|------|----------|
| MemoryRank | ✅ Signed |
| Panorama | ✅ Signed |

---

## 👤 Author

**GNJz (Qquarts)**
- GitHub: [@qquartsco-svg](https://github.com/qquartsco-svg)

---

## 🤝 Contributing

기여를 환영합니다! Issue나 Pull Request를 보내주세요.
