# MemoryRank Engine

> **연결된 데이터에서 "가장 중요한 것"을 찾아주는 랭킹 엔진**

MemoryRank는 Google **PageRank 알고리즘**을 기억/지식/문서 그래프에 응용한 엔진입니다.  
노드 간 연결 구조 + 최근성/정서/빈도를 종합하여 **중요도 점수**를 계산하고, 상위 N개를 추출합니다.

---

## 🎯 이런 문제를 해결합니다

| 상황 | MemoryRank가 하는 일 |
|------|---------------------|
| 수천 개의 문서 중 **핵심 문서 10개**만 뽑고 싶다 | 문서 간 참조 관계를 그래프로 만들고 중요도 순으로 정렬 |
| 검색 결과가 너무 많아서 **진짜 중요한 것**만 보고 싶다 | 검색 결과에 MemoryRank 점수를 곱해 재정렬 |
| 사용자 행동 로그에서 **가장 영향력 있는 이벤트**를 찾고 싶다 | 이벤트 연쇄 관계를 그래프로 만들고 핵심 노드 탐지 |
| PTSD 환자의 **침입 기억 패턴**을 분석하고 싶다 | 기억 네트워크에서 외상 관련 기억의 중요도 계산 |
| 추천 시스템에서 **핵심 아이템**을 선별하고 싶다 | 아이템 간 관계 그래프에서 영향력 높은 노드 추출 |

---

## 🚀 Quick Start (5분 안에 돌려보기)

### 1. 설치

```bash
git clone https://github.com/qquartsco-svg/memoryRank_engine.git
cd memoryRank_engine
pip install numpy
```

### 2. 바로 실행

```bash
python test_memoryrank_engine.py
```

### 3. 코드에서 사용

```python
from package.memoryrank import MemoryRankEngine, MemoryRankConfig, MemoryNodeAttributes

# 그래프 정의: (출발 노드, 도착 노드, 연결 강도)
edges = [
    ("문서A", "문서B", 1.0),
    ("문서B", "문서C", 1.0),
    ("문서C", "문서A", 0.5),
    ("문서C", "문서D", 0.8),
]

# 각 노드의 속성 (선택사항)
node_attrs = {
    "문서A": MemoryNodeAttributes(recency=0.3, emotion=0.4, frequency=0.5),
    "문서B": MemoryNodeAttributes(recency=0.5, emotion=0.5, frequency=0.5),
    "문서C": MemoryNodeAttributes(recency=0.9, emotion=0.9, frequency=0.9),  # 최근 + 중요
    "문서D": MemoryNodeAttributes(recency=0.2, emotion=0.2, frequency=0.2),
}

# 엔진 실행
engine = MemoryRankEngine(MemoryRankConfig())
engine.build_graph(edges, node_attrs)
scores = engine.calculate_importance()

# 결과 출력
for name, score in sorted(scores.items(), key=lambda x: -x[1]):
    print(f"{name}: {score:.4f}")
```

---

## 📊 출력 예시

```
문서C: 0.3892
문서B: 0.2541
문서A: 0.2233
문서D: 0.1334
```

→ **문서C**가 가장 높은 중요도 (연결도 많고, 최근성/정서/빈도도 높음)  
→ **문서D**는 연결이 적고 속성도 낮아서 최하위

---

## 💡 활용 사례

### 산업용 / 상업용

| 분야 | 적용 방법 |
|------|----------|
| **검색 엔진** | 키워드 매칭 후, MemoryRank로 "진짜 중요한" 결과만 상위 노출 |
| **추천 시스템** | 사용자 클릭/구매 로그 → 그래프 → 핵심 아이템 추천 |
| **콘텐츠 큐레이션** | 뉴스/블로그/영상 중 "가장 영향력 있는" 콘텐츠 자동 선별 |
| **로그 분석** | 서비스/IoT 로그에서 장애 원인이 된 핵심 이벤트 탐지 |
| **지식 관리** | 사내 위키/노트에서 핵심 문서 자동 식별 |

### 연구용

| 분야 | 적용 방법 |
|------|----------|
| **PTSD 연구** | 기억 네트워크에서 외상 기억의 "침입 가능성" 점수화 |
| **우울증 연구** | 부정 정서 기억의 "반추 루프 진입 가능성" 분석 |
| **ADHD 연구** | 작업 기억 그래프에서 주의 자원이 집중될 핵심 노드 예측 |
| **인지과학** | 기억 구조 변화가 "핵심 기억 집합"에 미치는 영향 실험 |
| **네트워크 과학** | damping/personalization 파라미터에 따른 중요도 분포 연구 |

---

## 📖 API 레퍼런스

### MemoryRankConfig

| 파라미터 | 기본값 | 설명 |
|---------|--------|------|
| `damping` | 0.85 | PageRank 감쇠 계수 (0~1) |
| `max_iter` | 100 | 최대 반복 횟수 |
| `tol` | 1e-6 | 수렴 판단 기준 |
| `recency_weight` | 1.0 | 최근성 가중치 |
| `emotion_weight` | 1.0 | 정서 강도 가중치 |
| `frequency_weight` | 1.0 | 빈도 가중치 |

### MemoryNodeAttributes

| 속성 | 범위 | 설명 |
|-----|------|------|
| `recency` | 0~1 | 최근일수록 1에 가까움 |
| `emotion` | 0~1 | 정서적으로 강렬할수록 높음 |
| `frequency` | 0~1 | 자주 등장/재생될수록 높음 |
| `base_importance` | ≥0 | 외부에서 직접 부여하는 추가 가중치 |

### MemoryRankEngine

| 메서드 | 설명 |
|--------|------|
| `build_graph(edges, node_attrs)` | 그래프 구성 |
| `calculate_importance()` | 중요도 계산 → `{node_id: score}` 반환 |
| `get_top_memories(k)` | 상위 k개 → `[(node_id, score), ...]` 반환 |

---

## 🔬 알고리즘 상세 (Google PageRank 기반)

### 핵심 아이디어

> "많은 중요한 노드로부터 참조되는 노드는 더 중요하다"

이 엔진은 Google이 웹 페이지 랭킹에 사용한 **PageRank 알고리즘**(Brin & Page, 1998)을 기반으로 합니다.  
여기에 **Personalized PageRank** 변형을 적용하여, 단순 연결 구조뿐 아니라 **최근성/정서/빈도**도 반영합니다.

### 수학적 정의

**PageRank 업데이트 식:**

```
r^{(t+1)} = α M r^{(t)} + (1 - α) v
```

- `M`: 전이 행렬 (열 정규화)
- `α`: damping factor (기본 0.85)
- `v`: personalization 벡터 (최근성/정서/빈도 반영)
- `r`: 랭크 벡터 (각 노드의 중요도)

**Personalization 벡터 계산:**

```
b_i = w_r × recency_i + w_e × emotion_i + w_f × frequency_i + base_importance_i
v_i = b_i / Σ_j b_j
```

**수렴 조건:** `||r^{(t+1)} - r^{(t)}||_1 < tol`

### 참고 논문

- Brin, S., & Page, L. (1998). *The anatomy of a large-scale hypertextual web search engine*. Computer Networks and ISDN Systems.

---

## 📄 라이선스

- **License**: MIT
- 이 엔진은 Google PageRank 알고리즘을 **메모리/지식 그래프 도메인에 응용**한 것입니다.

---

## ✅ PHAM 블록체인 서명

이 엔진은 **PHAM(Proof of Honest Authorship & Merit)** 시스템으로 서명되었습니다.

| 항목 | 값 |
|------|-----|
| 버전 | v1.0.0 |
| 서명 일자 | 2025-01-28 |
| 서명 도구 | `pham_sign_v4.py` |

### 서명된 파일

| 파일 | SHA-256 Hash | Score |
|------|--------------|-------|
| `memoryrank_engine.py` | `696d8760b66830bf5ea4a4b17880ddd30cf66922ddfe9418d037a277505f6840` | ⭐ A_HIGH |
| `README.md` | `1d4a989393130013910e13542ef956584611d3bbe13f0c03a6a9e6b394ddfb3e` | ⭐ A_HIGH |

상세 정보: `PHAM_BLOCKCHAIN_SIGNATURE.md` 참고

---

**Author**: GNJz (Qquarts)  
**Repository**: [github.com/qquartsco-svg/memoryRank_engine](https://github.com/qquartsco-svg/memoryRank_engine)
