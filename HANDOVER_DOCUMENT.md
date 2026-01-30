# 📋 Cognitive Kernel v2.0.1 인수인계 문서

> **작업 완료 상황 및 다음 작업 계획**

**작성일**: 2026-01-30  
**작성자**: GNJz (Qquarts)  
**버전**: 2.0.1

---

## 📊 프로젝트 개요

### 프로젝트명
**Cognitive Kernel** - 모듈형 인지 프레임워크

### 목적
기억의 시간 인코딩, 중요도 랭킹, 의사결정 반영을 결합한 모듈형 인지 프레임워크

### 핵심 가치
- **장기 기억**: 프로세스 종료 후에도 유지되는 영속성
- **중요도 랭킹**: Google PageRank 기반
- **의사결정**: Softmax Utility 기반
- **인지 모드**: ADHD, ASD, PTSD 등 다양한 인지 상태 시뮬레이션

---

## ✅ 완료된 작업 (2026-01-30 기준)

### 1. 핵심 엔진 구현 (7개)

#### 1.1 Panorama Memory Engine
- **기능**: 시간축 기억 저장 및 조회
- **알고리즘**: Ebbinghaus Forgetting Curve (지수 감쇠)
- **파일**: `src/cognitive_kernel/engines/panorama/`
- **상태**: ✅ 완료

#### 1.2 MemoryRank Engine
- **기능**: 기억 중요도 랭킹
- **알고리즘**: Personalized PageRank
- **파일**: `src/cognitive_kernel/engines/memoryrank/`
- **상태**: ✅ 완료

#### 1.3 Prefrontal Cortex (PFC) Engine
- **기능**: 의사결정, Working Memory
- **알고리즘**: Softmax Utility, Miller's Law
- **파일**: `src/cognitive_kernel/engines/pfc/`
- **상태**: ✅ 완료

#### 1.4 Basal Ganglia Engine
- **기능**: 습관 학습, 탐색-착취 균형
- **알고리즘**: Q-Learning
- **파일**: `src/cognitive_kernel/engines/basal_ganglia/`
- **상태**: ✅ 완료

#### 1.5 Thalamus Engine
- **기능**: 입력 필터링 (게이팅)
- **파일**: `src/cognitive_kernel/engines/thalamus/`
- **상태**: ✅ 기본 구현 완료 (게이팅 루프는 미구현)

#### 1.6 Amygdala Engine
- **기능**: 감정 처리, 위협 감지
- **알고리즘**: Rescorla-Wagner Model
- **파일**: `src/cognitive_kernel/engines/amygdala/`
- **상태**: ✅ 완료

#### 1.7 Hypothalamus Engine
- **기능**: 에너지 관리, 스트레스 처리
- **알고리즘**: HPA Axis Cortisol Dynamics
- **파일**: `src/cognitive_kernel/engines/hypothalamus/`
- **상태**: ✅ 기본 구현 완료 (PFC 통합은 미구현)

---

### 2. 통합 인터페이스

#### 2.1 CognitiveKernel 클래스
- **파일**: `src/cognitive_kernel/core.py`
- **주요 메서드**:
  - `remember()`: 기억 저장
  - `recall()`: 기억 회상 (PageRank 기반)
  - `decide()`: 의사결정 (PFC + BasalGanglia)
  - `learn_from_reward()`: 보상 학습
- **상태**: ✅ 완료

#### 2.2 세션 관리
- **자동 저장/로드**: Context Manager (`with` 문) 지원
- **영속성**: JSON, SQLite, NumPy NPZ 파일
- **상태**: ✅ 완료

---

### 3. 인지 모드 (Cognitive Modes)

#### 3.1 구현된 모드
- **NORMAL**: 균형잡힌 탐색/착취
- **ADHD**: 과도한 탐색 (고엔트로피)
- **ASD**: 과도한 착취 (저엔트로피)
- **PTSD**: 트라우마 고착

#### 3.2 파라미터 설정
- **파일**: `src/cognitive_kernel/cognitive_modes.py`
- **구조**: `ModeConfig` dataclass + `CognitiveModePresets`
- **상태**: ✅ 완료

---

### 4. 장기 기억 (Long-term Memory)

#### 4.1 구현 내용
- **Panorama**: 시간축 이벤트 저장
- **MemoryRank**: 중요도 그래프 저장
- **BasalGanglia**: Q-values 저장
- **자동 세션 관리**: Context Manager

#### 4.2 저장 형식
- JSON: 이벤트, 그래프, 메타데이터
- SQLite: 구조화된 데이터
- NumPy NPZ: 배열 데이터

#### 4.3 상태
- ✅ 완료

---

### 5. 이론적 분석 및 문서화

#### 5.1 최소 차분 모델
- **파일**: `docs/MINIMAL_DYNAMICS_MODEL.md`
- **내용**: 코드와 1:1 대응되는 수학적 정의
- **상태**: ✅ 완료

#### 5.2 물리적 동역학
- **파일**: `docs/PHYSICAL_DYNAMICS.md`
- **내용**: 자기장, 세차운동 분석
- **상태**: ✅ 완료

#### 5.3 안정 코어 이론
- **파일**: `docs/STABILITY_CORE.md`
- **내용**: 정신 안정의 최소 동역학 조건
- **상태**: ✅ 완료

#### 5.4 맥스웰 구조
- **파일**: `docs/MAXWELL_STRUCTURE.md`
- **내용**: 맥스웰 구조의 상태공간 이식
- **상태**: ✅ 완료

#### 5.5 인지 루프 분석
- **파일**: `docs/COGNITIVE_LOOPS_ANALYSIS.md`
- **내용**: 5가지 핵심 루프 분석
- **상태**: ✅ 완료

#### 5.6 편향 분석
- **파일**: `docs/COGNITIVE_BIAS_FIELD.md`
- **내용**: ADHD/ASD를 편향(+/-)으로 해석
- **상태**: ✅ 완료

---

### 6. 데모 및 예제

#### 6.1 인지 극성 데모
- **파일**: `examples/cognitive_polarity_demo.py`
- **내용**: ADHD vs ASD 동역학 비교
- **상태**: ✅ 완료 (규약 준수)

#### 6.2 세차운동 데모
- **파일**: `examples/precession_demo_v2.py`
- **내용**: 세차운동 시뮬레이션 (규약 준수)
- **상태**: ✅ 완료

#### 6.3 안정 코어 데모
- **파일**: `examples/stability_core_demo.py`
- **내용**: 안정 코어 시뮬레이션
- **상태**: ⚠️ 프로토타입 (규약 위반)

---

### 7. 배포 및 패키징

#### 7.1 PyPI 배포
- **패키지명**: `cognitive-kernel`
- **버전**: 2.0.1
- **상태**: ✅ 완료

#### 7.2 GitHub 릴리즈
- **버전**: v2.0.1
- **태그**: `v2.0.1`
- **상태**: ✅ 완료

---

## ⚠️ 알려진 한계점

### 1. API 한계

#### 1.1 전체 확률 분포 접근 불가
- **문제**: `decide()`는 단일 선택의 확률만 반환
- **영향**: 세차운동 데모에서 각 옵션에 대해 `decide()` 호출 필요
- **해결 방안**: 
  - `decide()` 반환값에 전체 확률 분포 추가
  - 또는 `get_probability_distribution()` 메서드 추가

#### 1.2 내부 메서드 의존
- **문제**: 일부 데모에서 `_calculate_memory_relevance()` 직접 호출
- **해결 방안**: 공개 API로 전환

---

### 2. 미구현 기능

#### 2.1 Thalamus 게이팅 루프
- **현재 상태**: 엔진은 있지만 `remember()` 경로를 거치지 않음
- **필요 작업**: `remember()` 메서드에 Thalamus 게이팅 통합

#### 2.2 Hypothalamus 통합
- **현재 상태**: 엔진은 있지만 PFC utility에 반영되지 않음
- **필요 작업**: 에너지/스트레스가 `decide()`에 영향 주도록 통합

#### 2.3 습관 덮어쓰기
- **현재 상태**: 충돌 flag만 존재
- **필요 작업**: 습관 강도가 임계값을 넘으면 PFC 결정을 덮어쓰는 로직

#### 2.4 `local_weight_boost` 구현
- **현재 상태**: 파라미터로만 존재
- **필요 작업**: MemoryRank 그래프 가중치에 실제 반영

---

### 3. 데모 코드 문제

#### 3.1 프로토타입 데모
- **파일**: `examples/precession_demo.py`, `examples/stability_core_demo.py`
- **문제**: 규약 위반 (내부 메서드 호출, 하드코딩)
- **해결**: 규약 준수 버전 작성 필요

---

## 🚀 다음 작업 계획

### 우선순위 1: API 개선

#### 1.1 전체 확률 분포 접근
- **작업**: `decide()` 반환값 확장
- **예상 시간**: 2-3시간
- **파일**: `src/cognitive_kernel/core.py`

**구현 방안:**
```python
def decide(...) -> Dict[str, Any]:
    ...
    return {
        "action": ...,
        "utility": ...,
        "probability": ...,  # 단일 선택 확률
        "probability_distribution": {  # NEW: 전체 분포
            opt: prob for opt, prob in zip(options, probabilities)
        },
        ...
    }
```

---

#### 1.2 공개 API 정리
- **작업**: 내부 메서드를 공개 API로 전환
- **예상 시간**: 1-2시간
- **파일**: `src/cognitive_kernel/core.py`

**구현 방안:**
```python
def calculate_memory_relevance(
    self,
    option: str,
    memories: Optional[List[Dict]] = None,
) -> float:
    """공개 API: 옵션과 기억의 관련성 계산"""
    if memories is None:
        memories = self.recall(k=self.config.working_memory_capacity)
    ...
```

---

### 우선순위 2: 엔진 통합 완성

#### 2.1 Thalamus 게이팅 루프
- **작업**: `remember()` 메서드에 Thalamus 게이팅 통합
- **예상 시간**: 3-4시간
- **파일**: `src/cognitive_kernel/core.py`

**구현 방안:**
```python
def remember(self, ...):
    # Thalamus 게이팅
    filtered_input = self.thalamus.gate(
        input_data,
        threshold=self.mode_config.gate_threshold,
        max_channels=self.mode_config.max_channels,
    )
    
    if filtered_input:
        # Panorama에 저장
        ...
```

---

#### 2.2 Hypothalamus 통합
- **작업**: 에너지/스트레스가 PFC utility에 반영
- **예상 시간**: 2-3시간
- **파일**: `src/cognitive_kernel/core.py`

**구현 방안:**
```python
def decide(self, ...):
    ...
    # Hypothalamus 패널티
    stress_penalty = self.hypothalamus.get_stress() * 0.3
    energy_cost = (1.0 - self.hypothalamus.get_energy()) * 0.2
    
    utility = expected_reward - stress_penalty - energy_cost
    ...
```

---

#### 2.3 습관 덮어쓰기
- **작업**: 습관 강도가 임계값을 넘으면 PFC 결정 덮어쓰기
- **예상 시간**: 2-3시간
- **파일**: `src/cognitive_kernel/core.py`

**구현 방안:**
```python
def decide(self, ...):
    ...
    habit_action = self.basal_ganglia.select_action(context, options)
    habit_strength = self.basal_ganglia.get_habit_strength(context, habit_action)
    
    if habit_strength > self.config.habit_override_threshold:
        return {
            "action": habit_action,
            "source": "habit_override",
            ...
        }
    ...
```

---

### 우선순위 3: MemoryRank 개선

#### 3.1 `local_weight_boost` 구현
- **작업**: MemoryRank 그래프 가중치에 실제 반영
- **예상 시간**: 4-5시간
- **파일**: `src/cognitive_kernel/engines/memoryrank/`

**구현 방안:**
```python
def _calculate_edge_weight(self, node1, node2, ...):
    base_weight = ...
    if self.config.local_weight_boost > 1.0:
        # 로컬 연결 강화 (ASD)
        if self._is_local_connection(node1, node2):
            weight = base_weight * self.config.local_weight_boost
    ...
```

---

### 우선순위 4: 데모 코드 정리

#### 4.1 규약 준수 데모 작성
- **작업**: 모든 데모를 규약 준수 버전으로 전환
- **예상 시간**: 3-4시간
- **파일**: `examples/`

**규약:**
- `kernel.decide()` 직접 사용
- 세션 격리 (uuid 기반)
- 공개 API만 사용
- CONFIG로 파라미터화

---

### 우선순위 5: 테스트 및 검증

#### 5.1 통합 테스트
- **작업**: 전체 파이프라인 테스트
- **예상 시간**: 4-5시간
- **파일**: `tests/`

#### 5.2 성능 벤치마크
- **작업**: 대규모 데이터셋 테스트
- **예상 시간**: 2-3시간

---

## 📁 프로젝트 구조

```
Cognitive_Kernel/
├── src/
│   └── cognitive_kernel/
│       ├── __init__.py
│       ├── core.py                    # 메인 클래스
│       ├── cognitive_modes.py         # 인지 모드
│       └── engines/
│           ├── panorama/
│           ├── memoryrank/
│           ├── pfc/
│           ├── basal_ganglia/
│           ├── thalamus/
│           ├── amygdala/
│           └── hypothalamus/
├── examples/
│   ├── cognitive_polarity_demo.py     # ✅ 규약 준수
│   ├── precession_demo_v2.py         # ✅ 규약 준수
│   ├── precession_demo.py            # ⚠️ 프로토타입
│   └── stability_core_demo.py        # ⚠️ 프로토타입
├── docs/
│   ├── MINIMAL_DYNAMICS_MODEL.md
│   ├── PHYSICAL_DYNAMICS.md
│   ├── STABILITY_CORE.md
│   ├── MAXWELL_STRUCTURE.md
│   ├── COGNITIVE_LOOPS_ANALYSIS.md
│   ├── COGNITIVE_BIAS_FIELD.md
│   ├── COGNITIVE_STATES.md
│   ├── COGNITIVE_DYSFUNCTION.md
│   └── DEMO_LIMITATIONS.md
├── tests/
├── README.md
├── pyproject.toml
└── HANDOVER_DOCUMENT.md              # 이 문서
```

---

## 🔧 개발 환경

### 필수 요구사항
- Python 3.9+
- NumPy
- SQLite3 (표준 라이브러리)

### 설치 방법
```bash
pip install cognitive-kernel
```

### 개발 모드 설치
```bash
cd /Users/jazzin/Desktop/00_BRAIN/Cognitive_Kernel
pip install -e .
```

---

## 📚 주요 문서

### 사용자 문서
- `README.md`: 프로젝트 개요 및 사용법
- `docs/COGNITIVE_STATES.md`: 인지 모드 상세 설명
- `docs/LONG_TERM_MEMORY.md`: 장기 기억 설명

### 개발자 문서
- `docs/MINIMAL_DYNAMICS_MODEL.md`: 수학적 모델
- `docs/PHYSICAL_DYNAMICS.md`: 물리적 동역학
- `docs/STABILITY_CORE.md`: 안정 코어 이론
- `docs/COGNITIVE_LOOPS_ANALYSIS.md`: 루프 분석

### 한계점 문서
- `docs/DEMO_LIMITATIONS.md`: 데모 코드 한계점

---

## 🎯 핵심 수식 (v2.0.1)

### 최소 차분 모델

$$
\begin{align}
C_n(k) &= \min\left(1, \sum_{i} s_i \cdot m_{i,k}\right) \\
U_{n,k} &= U_0 + \alpha \cdot C_n(k) \\
P_n(k) &= \frac{\exp(\beta \cdot U_{n,k})}{\sum_j \exp(\beta \cdot U_{n,j})} \\
E_n &= -\sum_{k} P_n(k) \ln P_n(k)
\end{align}
$$

**변수:**
- $s_i$: recall() 반환 중요도 (MemoryRank score)
- $m_{i,k}$: 텍스트 키워드 매칭
- $\beta$: decision_temperature
- $\alpha$: 기억 영향 계수 (0.5)
- $U_0$: 기본 보상 (0.5)

---

## 🔗 관련 리소스

### GitHub
- **Repository**: `qquartsco-svg/Cognitive_Kernel`
- **Latest Release**: v2.0.1

### PyPI
- **Package**: `cognitive-kernel`
- **Version**: 2.0.1

---

## 📞 연락처

**Author**: GNJz (Qquarts)  
**Email**: (GitHub 프로필 참조)

---

## 📝 변경 이력

### v2.0.1 (2026-01-30)
- ✅ 7개 엔진 통합 완료
- ✅ 인지 모드 구현 (ADHD, ASD, PTSD)
- ✅ 장기 기억 구현
- ✅ 물리적 동역학 분석
- ✅ 규약 준수 데모 작성

### v1.0.0 (이전)
- 초기 릴리즈

---

## 🎓 학습 자료

### 추천 읽기 순서
1. `README.md` - 프로젝트 개요
2. `docs/MINIMAL_DYNAMICS_MODEL.md` - 수학적 모델
3. `docs/COGNITIVE_STATES.md` - 인지 모드
4. `examples/cognitive_polarity_demo.py` - 사용 예제

### 심화 학습
- `docs/PHYSICAL_DYNAMICS.md` - 물리적 동역학
- `docs/STABILITY_CORE.md` - 안정 코어 이론
- `docs/COGNITIVE_LOOPS_ANALYSIS.md` - 루프 분석

---

**마지막 업데이트**: 2026-01-30  
**다음 리뷰 예정일**: (미정)

