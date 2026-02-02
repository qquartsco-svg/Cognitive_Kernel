# Boundary Convergence Engine 설계 문서

**작성일**: 2026-02-01  
**목적**: 경계-공간 정합 계수로서의 π 개념을 구현하는 엔진 설계

---

## ⚠️ 핵심 명확화

**이 엔진은 π를 계산하는 것이 아니라, 경계-공간 정합의 동역학적 과정을 구현합니다.**

- ❌ π 계산 알고리즘
- ❌ 수치적 근사 엔진
- ✅ **경계-공간 정합 계수**로서의 π 개념 구현
- ✅ 연속 공간 채움의 동역학적 과정 계산

---

## 1. 엔진 정체성

### 이름 후보

1. **BoundaryConvergenceEngine** (권장)
   - 경계 수렴 엔진
   - 명확하고 기술적

2. **SpatialFillConvergenceEngine**
   - 공간 채움 수렴 엔진
   - 기능 중심

3. **ContinuumAlignmentEngine**
   - 연속체 정렬 엔진
   - 수학적 정확성

4. **BoundaryDensityEngine**
   - 경계 밀도 엔진
   - 간결함

**최종 선택**: `BoundaryConvergenceEngine`

---

## 2. 핵심 개념

### π의 재정의

**기존 관점**:
```
π = 3.14159... (상수)
```

**본 엔진의 관점**:
```
π = 경계(선)와 내부 공간(면)의 정합 계수
```

**엔지니어링 언어**:
- 경계 추정 문제 (Boundary Estimation)
- 연속 공간 근사 문제 (Continuous Filling)
- 오차 수렴 루프 (Asymptotic Convergence Loop)

---

## 3. 핵심 구성 요소

### 3.1 Boundary Generator (경계 생성기)

**기능**:
- 초기 원형 경계 생성 (거친 다각형)
- 점 개수 N 설정
- 경계 점 좌표 생성

**수식**:
```
P_i = (r * cos(2πi/N), r * sin(2πi/N))
```

**코드 구조**:
```python
class BoundaryGenerator:
    def generate_initial_boundary(self, n_points: int, radius: float) -> List[Point]:
        """초기 경계 생성"""
        pass
```

---

### 3.2 Interior Density Estimator (내부 밀도 추정기)

**기능**:
- 경계 내부를 점/셀로 채움
- 밀도 함수 D(r, θ) 계산
- 공간 채움 정도 측정

**수식**:
```
D(r, θ) = Σ importance_i * exp(-k * distance(r, θ, point_i))
```

**코드 구조**:
```python
class InteriorDensityEstimator:
    def estimate_density(self, boundary: List[Point], interior_points: List[Point]) -> float:
        """내부 밀도 추정"""
        pass
```

---

### 3.3 Mismatch Calculator (불일치 계산기)

**기능**:
- 경계 길이 vs 내부 면적 간 불일치 계산
- 오차 Δ 계산
- 수렴 목표 설정

**수식**:
```
Δ = |perimeter_estimate - 2π * radius| + |area_estimate - π * radius²|
```

**코드 구조**:
```python
class MismatchCalculator:
    def calculate_mismatch(self, perimeter: float, area: float, radius: float) -> float:
        """불일치 계산"""
        pass
```

---

### 3.4 Boundary Refinement Loop (경계 정제 루프)

**기능**:
- 경계 점 수 증가
- 곡률 재분배
- Δ 최소화

**알고리즘**:
```
1. 초기 경계 생성 (N=4)
2. 내부 밀도 추정
3. 불일치 계산
4. 경계 점 수 증가 (N *= 2)
5. 곡률 재분배
6. 2-5 반복 (Δ < threshold까지)
```

**코드 구조**:
```python
class BoundaryRefinementLoop:
    def refine(self, initial_boundary: List[Point], threshold: float) -> ConvergenceResult:
        """경계 정제"""
        pass
```

---

### 3.5 Convergence Controller (수렴 제어기)

**기능**:
- 수렴률 계산
- 임계 오차 설정
- iteration 제한

**파라미터**:
- `convergence_rate`: 수렴 속도
- `error_threshold`: 임계 오차
- `max_iterations`: 최대 반복 횟수

**코드 구조**:
```python
class ConvergenceController:
    def check_convergence(self, mismatch: float, iteration: int) -> bool:
        """수렴 확인"""
        pass
```

---

## 4. 엔진 출력

### 출력 구조

**❌ 출력 = π 값** (이건 의미 없음)

**✅ 출력 = 수렴 과정**

```python
@dataclass
class ConvergenceResult:
    """수렴 과정 결과"""
    iteration: int  # 반복 횟수
    boundary_points: int  # 경계 점 개수
    perimeter_estimate: float  # 경계 길이 추정값
    area_estimate: float  # 면적 추정값
    mismatch: float  # 불일치 오차
    convergence_rate: float  # 수렴률
    density_map: Dict[Point, float]  # 밀도 맵
    history: List[ConvergenceState]  # 수렴 히스토리
```

**의미**:
- "원은 이렇게 만들어진다"
- "공간은 이렇게 채워진다"
- "π는 결과가 아니라 과정이다"

---

## 5. 모듈 구조

```
src/cognitive_kernel/engines/boundary_convergence/
├── __init__.py
├── boundary_convergence_engine.py  # 메인 엔진
├── boundary_generator.py            # 경계 생성기
├── density_estimator.py            # 밀도 추정기
├── mismatch_calculator.py           # 불일치 계산기
├── refinement_loop.py              # 정제 루프
├── convergence_controller.py       # 수렴 제어기
├── config.py                        # 설정
└── models.py                        # 데이터 모델
```

---

## 6. 기존 엔진과의 차별점

### 기존 수학 라이브러리

```
π = 상수 (3.14159...)
결과 중심
의미 없음
```

### 본 엔진

```
π = 경계-공간 상호작용의 부산물
과정 중심
물리·인지·공간 모델링에 바로 사용 가능
```

---

## 7. 활용 분야

### 7.1 인지 엔진 (현재 프로젝트)

- 기억 경계 형성
- 개념 내부 밀도 형성
- 코어-주변 구조

### 7.2 의료 / 생물

- 세포막 형성
- 종양 성장 경계
- 뇌 영역 분화

### 7.3 물리 / 우주

- 사건지평선
- 중력 퍼텐셜 경계
- 위상 공간 생성

### 7.4 산업

- 메시 생성
- 연속 공간 근사
- FEM / CFD 전처리

---

## 8. Cognitive Kernel 통합

### 8.1 Dynamics Engine과의 관계

**Dynamics Engine**:
- 회전과 감쇠에 집중
- 위상 공간 샘플링

**Boundary Convergence Engine**:
- 경계-공간 정합
- 밀도 형성 과정

**통합**:
```python
# Dynamics Engine의 precession_phi를 경계 생성에 활용
boundary = boundary_engine.generate_boundary(
    n_points=int(precession_phi * 100),  # 위상에 따라 점 개수 조절
    radius=core_strength  # 코어 강도를 반지름으로
)
```

### 8.2 MemoryRank Engine과의 관계

**MemoryRank Engine**:
- 기억의 중요도 랭킹
- 그래프 구조

**Boundary Convergence Engine**:
- 기억 경계 형성
- 내부 밀도 계산

**통합**:
```python
# 기억의 중요도를 밀도로 변환
density_map = boundary_engine.estimate_density(
    boundary=memory_boundary,
    interior_points=memories,
    importance_weights=memoryrank.get_importance_scores()
)
```

---

## 9. 구현 우선순위

### Phase 1: 핵심 구조 (1-2주)

1. Boundary Generator 구현
2. Mismatch Calculator 구현
3. 기본 수렴 루프 구현

### Phase 2: 밀도 추정 (1주)

1. Interior Density Estimator 구현
2. 밀도 맵 생성
3. 시각화 기능

### Phase 3: 고급 기능 (1-2주)

1. Convergence Controller 고도화
2. 다양한 경계 형태 지원
3. 병렬 처리 최적화

### Phase 4: 통합 (1주)

1. Dynamics Engine 통합
2. MemoryRank Engine 통합
3. Cognitive Kernel 통합

---

## 10. 테스트 전략

### 10.1 수학적 정확성

- 경계 길이 vs 면적 정합 검증
- 수렴률 측정
- 오차 범위 확인

### 10.2 물리적 일관성

- 밀도 보존 검증
- 경계 연속성 확인
- 수렴 안정성 테스트

### 10.3 인지 모델 적용

- 기억 경계 형성 테스트
- 코어 밀도 계산 검증
- 치매/알츠하이머 모델 통합

---

## 11. 문서화 요구사항

### 필수 명확화

1. **π를 계산하지 않음** 명시
2. **경계-공간 정합** 개념 설명
3. **구조적 유사성** vs **물리적 동일성** 구분
4. **과정 중심** 출력 설명

### 테스트 이름

**기존**: "원주율 수렴 테스트"

**권장**: "Continuous Space Filling via Phase Precession"

---

## 12. LLM 통합 타이밍

**현재 단계**: ❌ LLM 통합 금지

**이유**:
- 이 구조는 이미 자립적인 물리 커널
- 설명 대상이지, 설명자 아님
- LLM은 "이 공간이 왜 이렇게 채워졌는지 설명하는 층"
- 지금 붙이면 가치가 희석됨

**통합 시점**:
- 엔진이 완전히 독립적으로 작동할 때
- 물리적 정당성이 검증된 후
- 상위 계층(설명/언어화)이 필요할 때

---

## 결론

**Boundary Convergence Engine**은:
- ❌ π 계산기 아님
- ✅ 경계-공간 정합의 동역학적 과정 구현
- ✅ 연속 공간에서 의미가 형성되는 과정 계산
- ✅ Cognitive Kernel의 8번째 엔진 후보

**핵심 가치**:
- 과정 중심의 물리적 모델
- 인지·의료·산업 모두에 적용 가능
- 기존 수학 라이브러리와 차별화

---

**작성자**: GNJz (Qquarts)  
**작성일**: 2026-02-01  
**버전**: 설계 v1.0.0

