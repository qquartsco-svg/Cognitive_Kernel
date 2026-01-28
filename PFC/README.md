# PFC Engine (Prefrontal Cortex)

> **"무엇을 기억하고, 어떻게 행동할지 결정하는 감독"** — 작업 기억 + 행동 선택 + 억제 엔진

---

## 🎬 기억의 영화관에서의 역할

```
┌─────────────────────────────────────────────────────────────┐
│                    🧠 Cognitive Kernel                       │
├─────────────────────────────────────────────────────────────┤
│   🎞️ Panorama (필름)    →   "무슨 일이 있었나"               │
│   💡 MemoryRank (조광기) →   "뭐가 중요한가"                  │
│   🎬 PFC (영사기+감독)   →   "어떻게 할 것인가" ← 이 엔진     │
└─────────────────────────────────────────────────────────────┘
```

---

## 핵심 기능 (v1.0)

| 기능 | 설명 | 수식 |
|------|------|------|
| **Working Memory** | 중요 정보 임시 저장 (Miller's Law: 7±2) | capacity eviction |
| **Action Evaluator** | 행동의 기대 효용 계산 | U = r - c - risk×κ |
| **Inhibitor** | 위험한 행동 억제 (Go/No-Go) | conflict > threshold |
| **Selector** | Softmax 확률적 선택 | P(i) = exp(βU_i) / Σexp(βU_j) |

---

## Quick Start

\`\`\`python
from pfc import PFCEngine, PFCConfig, Action

# 엔진 초기화
pfc = PFCEngine(PFCConfig(
    working_memory_capacity=7,
    risk_aversion=0.5,
    inhibition_threshold=0.7,
    decision_temperature=1.0,
))

# MemoryRank 결과 로드
top_memories = [("memory_001", 0.45), ("memory_002", 0.30)]
pfc.load_from_memoryrank(top_memories)

# 행동 후보 정의
actions = [
    Action.create("rest", reward=0.6, cost=0.1, risk=0.05),
    Action.create("work", reward=0.8, cost=0.5, risk=0.2),
    Action.create("risky", reward=0.9, cost=0.4, risk=0.8),
]

# 통합 처리
result = pfc.process(
    candidate_actions=actions,
    goal="complete daily tasks",
)

if result.inhibited:
    print("행동 억제됨")
else:
    print(f"선택: {result.action.name}, 효용: {result.utility:.3f}")
\`\`\`

---

## Output Example

\`\`\`
============================================================
PFC Engine v1.0 - Test (영사기 + 감독)
============================================================

[1] Working Memory 테스트 (Miller's Law: 용량 5)
  로드된 기억 수: 5 (용량: 5)
    - memory_trauma_001: relevance=0.900
    - memory_yesterday_lunch: relevance=0.600

[2] 행동 후보 효용 평가
  rest: U = 0.475 (r=0.6, c=0.1, risk=0.05)
  work: U = 0.200 (r=0.8, c=0.5, risk=0.2)
  risky_adventure: U = 0.100 (r=0.9, c=0.4, risk=0.8)

[3] 억제(Inhibition) 테스트
  'risky_adventure' 억제 여부: True
  갈등 신호: 0.800 (threshold: 0.6)

[4] Softmax 행동 선택
  rest: 42.4%
  work: 24.5%
  socialize: 33.1%

✅ PFC Engine 테스트 완료
\`\`\`

---

## API Reference

### PFCConfig

| 파라미터 | 타입 | 기본값 | 설명 |
|---------|------|-------|------|
| working_memory_capacity | int | 7 | Miller's Law 용량 |
| decay_rate | float | 0.1 | 작업 기억 감쇠율 |
| risk_aversion | float | 0.5 | 위험 회피 계수 (κ) |
| inhibition_threshold | float | 0.7 | 억제 임계값 |
| decision_temperature | float | 1.0 | Softmax 온도 (β) |

### PFCEngine

| 메서드 | 설명 |
|--------|------|
| load_to_working_memory() | 작업 기억에 항목 추가 |
| load_from_memoryrank() | MemoryRank 결과 로드 |
| evaluate_action() | 행동 효용 계산 |
| should_inhibit() | 억제 여부 판단 |
| select_action() | Softmax 행동 선택 |
| process() | 통합 파이프라인 |

---

## Algorithm Details

### Expected Utility

\`\`\`
U(action) = expected_reward - effort_cost - risk × risk_aversion
\`\`\`

### Softmax Selection

\`\`\`
P(action_i) = exp(β × U_i) / Σ exp(β × U_j)

β = decision_temperature
\`\`\`

### Working Memory Decay

\`\`\`
relevance(t) = relevance_0 × exp(-λ × Δt)
\`\`\`

---

## 활용 시나리오

| 분야 | 활용 |
|------|------|
| **AI 에이전트** | 대화 맥락 유지, 행동 결정 |
| **ADHD 시뮬레이션** | 작업 기억 용량 감소, 억제 약화 |
| **우울증 시뮬레이션** | 행동 효용 왜곡, 무기력 |
| **게임 NPC** | 목표 기반 행동 선택 |

---

## License

MIT License

---

## PHAM Blockchain Signature

| 항목 | 값 |
|------|---|
| Author | GNJz (Qquarts) |
| Date | 2025-01-29 |
| Version | v1.0.0 |
