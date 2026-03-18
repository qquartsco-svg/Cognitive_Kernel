# irrational_algebra

**무리수-대수 구조 해석 엔진**

> 값이 무엇인지보다,  
> 지금 상태가 어떤 비율 구조를 이루고 있는지가 더 중요할 때가 있다.

---

## 정체성

이 엔진은 무리수를 계산하지 않는다.  
또 수렴 과정을 직접 생성하지도 않는다.

이 엔진의 역할은 **현재 상태 벡터가 어떤 무리수 구조에 가까운지 해석**하는 것이다.

| 엔진 | 역할 |
|---|---|
| `AlgebraApprox_Engine` | 근사 방법론 |
| `IrrationalApprox_Engine` | 무리수 수렴 생성 |
| `ConvergenceDynamics_Engine` | 수렴 과정 판정 |
| **`irrational_algebra`** | 현재 상태 구조 해석 |

즉 `irrational_algebra`는 수학 4엔진 축의 마지막 해석기다.

---

## 핵심 기능

| 기능 | 설명 |
|---|---|
| ratio resonance | 상태 벡터의 인접 비율이 `π`, `√2`, `φ`, `e` 중 어디에 가까운지 측정 |
| algebraic invariants | `φ² - φ - 1 = 0`, `x² - 2 = 0` 같은 대수적 닫힘 정도 계산 |
| boundary alignment | `Boundary_Convergence_Engine`의 mismatch를 구조 건강도에 반영 |
| observer alignment | `Observer Ω`를 구조 건강도에 반영 |
| dynamics alignment | `ConvergenceDynamics_Engine`의 `dynamic_health`를 구조 건강도에 반영 |

---

## 빠른 시작

```python
from cognitive_kernel.engines.irrational_algebra import IrrationalAlgebraEngine

engine = IrrationalAlgebraEngine()

snapshot = engine.analyze(
    [3.14, 1.0, 1.618],
    observer_omega=0.82,
    boundary_mismatch=0.05,
    dynamic_health=0.91,
)

print(snapshot.dominant_constant)
print(snapshot.structural_health)
```

---

## 구조 건강도

`structural_health`는 다섯 축의 가중 합으로 계산된다.

```text
ratio_weight
+ invariant_weight
+ boundary_weight
+ observer_weight
+ dynamics_weight
= 1.0
```

현재 기본값:
- ratio: 0.25
- invariant: 0.25
- boundary: 0.20
- observer: 0.15
- dynamics: 0.15

즉 이 엔진은 정적 비율 구조만 보지 않고,
경계 정합과 관측 건강도, 수렴 동역학까지 묶어서 최종 구조 건강도를 만든다.

---

## 4엔진 구조 내 위치

```text
AlgebraApprox_Engine         → 근사 도구
IrrationalApprox_Engine     → 수렴 생성기
ConvergenceDynamics_Engine  → 수렴 판정기
irrational_algebra          → 구조 해석기  ← 여기
```

브레인 상태공간 관점에서는 이렇게 해석할 수 있다.
- `AlgebraApprox`: 왜 근사가 통하는가
- `IrrationalApprox`: 어떤 수열로 무리수에 도달하는가
- `ConvergenceDynamics`: 그 도달 과정이 안정적인가
- `irrational_algebra`: 지금 상태가 어떤 구조적 질서를 갖는가

---

## 파일 구조

```text
irrational_algebra/
├── __init__.py
├── config.py
├── irrational_algebra_engine.py
├── models.py
├── README.md
├── BLOCKCHAIN_INFO.md
└── PHAM_BLOCKCHAIN_LOG.md
```

테스트:
- `tests/test_irrational_algebra_engine.py`

---

## 🔐 PHAM 블록체인 서명

| 항목 | 내용 |
|------|------|
| **라이선스** | MIT License |
| **기여도 상한** | GNJz(Qquarts) 자발적 기여도 제한 — 블록체인 기반 최대 6% |
| **검증 방법** | 블록체인으로 기여도·출처 영구 기록 및 검증 가능 |
| **사용 제한** | 없음 (MIT) |

> 서명 상세: [BLOCKCHAIN_INFO.md](./BLOCKCHAIN_INFO.md)
