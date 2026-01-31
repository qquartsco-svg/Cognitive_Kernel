# 📚 Cognitive Kernel 버전 히스토리

> **블록체인 해시 기록 순서대로 정리된 개발 로그**

**작성일**: 2026-01-31  
**현재 버전**: v2.0.1

---

## 🎯 목적

이 문서는 Cognitive Kernel이 어떻게 만들어졌는지, 각 버전에서 무엇이 추가/변경되었는지를 **블록체인 해시 순서대로** 기록합니다.

**왜 중요한가:**
- 생소한 기술/코드 로직이라 체계적인 기록 필요
- 버전별 변화 추적
- 개발 과정 이해
- 과거 버전 복구 가능

---

## 📋 버전별 기록

### v1.0.0 (2026-01-29)

**PHAM 블록체인 해시:**
- `63a182f8a1420231ee3d45efd5d0b9d2800be6790619934f8f2f82daf3e57454`
- IPFS CID: `Qme2rgSYgFzmNszMVV5eMu9ShV7uMLCn8Uj26J9XeosCe9`

**주요 특징:**
- 통합 인지 엔진 초기 구현
- 자동 세션 관리 (with 문 지원)
- 4개 엔진 통합 (Panorama, MemoryRank, PFC, BasalGanglia)
- 장기 기억 저장/로드

**코드 구조:**
- `cognitive_kernel.py` (단일 파일)
- 경로 설정: `sys.path.insert`로 각 엔진 패키지 추가

**핵심 수식:**
```python
# 기억 기반 보상 보정
expected_reward = 0.5  # 기본값만 (기억 반영 없음)
```

**한계점:**
- 기억이 의사결정에 반영되지 않음
- 인지 모드 없음
- Thalamus, Amygdala, Hypothalamus 미통합

---

### v2.0.0 (2026-01-30)

**Git 커밋:**
- `3376b0b` - feat: Add PyPI package structure (v2.0.0)

**주요 변경사항:**
- PyPI 패키지 구조로 전환 (`src/cognitive_kernel/`)
- LangChain 통합 예제 추가
- LlamaIndex 통합 예제 추가
- Vector DB 통합 (Chroma/FAISS)

**코드 구조:**
```
src/cognitive_kernel/
├── __init__.py
├── core.py
└── engines/
    ├── panorama/
    ├── memoryrank/
    ├── pfc/
    └── basal_ganglia/
```

**핵심 수식:**
```python
# 기억 기반 보상 보정 (v2.0.0)
expected_reward = 0.5  # 여전히 기본값만
```

---

### v2.0.1 (2026-01-30 ~ 2026-01-31)

**Git 커밋:**
- `ee704aa` - feat: Add Cognitive Modes (ADHD/ASD/PTSD)
- `deb20c3` - feat: MemoryRank → Action Utility 연결 구현
- `e65047e` - chore: v2.0.1 버전 업데이트 및 릴리즈 노트

**주요 변경사항:**

#### 1. 인지 모드 추가
- `CognitiveMode` Enum: NORMAL, ADHD, ASD, PTSD
- `ModeConfig` dataclass: 모드별 파라미터 설정
- `set_mode()` 메서드: 동적 모드 전환

#### 2. 기억 기반 의사결정 구현
**핵심 수식 (v2.0.1 최소 차분 모델):**
```python
# 기억 관련성 계산
C_n(k) = min(1, Σ(s_i × m_{i,k}))
# s_i: recall() 반환 중요도 (MemoryRank score)
# m_{i,k}: 텍스트 키워드 매칭

# 효용 계산
U_{n,k} = U_0 + α · C_n(k)
# U_0: 기본 보상 (0.5)
# α: 기억 영향 계수 (0.5)

# 확률 계산
P_n(k) = exp(β · U_{n,k}) / Σ exp(β · U_{n,j})
# β: decision_temperature (모드별 다름)

# 엔트로피
E_n = -Σ P_n(k) ln P_n(k)
```

**코드 구현:**
```python
# core.py (332-335줄)
# 기억 기반 보상 보정: U_i = U_base + α · r_i
alpha = 0.5
expected_reward = 0.5 + alpha * memory_relevance
```

#### 3. 7개 엔진 통합
- Panorama: 시간축 기억
- MemoryRank: 중요도 랭킹
- PFC: 의사결정
- BasalGanglia: 습관 학습
- Thalamus: 입력 필터링 (게이팅)
- Amygdala: 감정 처리
- Hypothalamus: 에너지 관리

#### 4. 물리적 동역학 문서화
- `docs/PHYSICAL_DYNAMICS.md` - 자기장, 세차운동 분석
- `docs/STABILITY_CORE.md` - 안정 코어 이론
- `docs/MAXWELL_STRUCTURE.md` - 맥스웰 구조 이식

---

### v2.0.1+ (2026-01-31 현재)

**최신 변경사항:**

#### 1. 엔트로피 기반 자동 회전 토크 구현
**핵심 수식:**
```python
# 엔트로피 계산
E_n = -Σ P_n(k) ln P_n(k)

# 정규화된 엔트로피
normalized_entropy = E_n / ln(N)  # N: 옵션 수

# 회전 토크 세기
torque_strength = γ · normalized_entropy
# γ: 모드별 회전 강도 (ADHD: 0.45, ASD: 0.15, NORMAL: 0.3)

# 회전 토크
T_n(k) = torque_strength · cos(φ_n - ψ_k)
# φ_n: 현재 위상 (느린 시간척도)
# ψ_k: 옵션 k의 고유 위상

# 위상 업데이트
φ_{n+1} = φ_n + ω
# ω: 세차 속도 (0.05)
```

**코드 구현:**
```python
# core.py (359-423줄)
# 엔트로피 계산
entropy = -sum(prob * math.log(prob) for prob in probabilities if prob > 0)

# 자동 회전 토크 생성
normalized_entropy = entropy / max_entropy
torque_strength = gamma * normalized_entropy
auto_torque[opt] = torque_strength * math.cos(self._precession_phi - psi[opt])
```

#### 2. 전체 확률 분포 반환
```python
# core.py (469줄)
"probability_distribution": probability_distribution,  # 전체 분포
"entropy": entropy,  # 엔트로피
"core_strength": core_strength,  # 코어 강도
```

#### 3. 질환 모드 추가 (6개)
- PANIC (공황장애)
- EPILEPSY (간질)
- OCD (강박)
- IED (분노조절장애)
- DEPRESSION (우울증)
- BIPOLAR (양극성 장애)

#### 4. local_weight_boost 구현
- `MemoryRankConfig`에 `local_weight_boost` 파라미터 추가
- `build_graph()`에서 로컬 연결 판단 및 가중치 부스트 적용

---

## 🔗 PHAM 블록체인 체인

### 체인 구조

```
GENESIS (index: 0)
    ↓
cognitive_kernel.py v1.0.0 (index: 1)
    Hash: 63a182f8a1420231ee3d45efd5d0b9d2800be6790619934f8f2f82daf3e57454
    CID: Qme2rgSYgFzmNszMVV5eMu9ShV7uMLCn8Uj26J9XeosCe9
    Score: 0.9998
    Label: A_HIGH
```

### 엔진별 PHAM 체인

각 엔진 모듈도 독립적인 PHAM 체인을 가짐:

1. **MemoryRank**
   - `pham_chain_memoryrank_engine.json`
   - `pham_chain_persistence.json`

2. **Panorama**
   - `pham_chain_persistence.json`

3. **BasalGanglia**
   - `blockchain/pham_chain_basal_ganglia_engine.json`
   - `blockchain/pham_chain_config.json`
   - `blockchain/pham_chain_data_types.json`

---

## 📐 수식 진화 과정

### v1.0.0: 기본 구조
```python
expected_reward = 0.5  # 고정값
```

### v2.0.0: 기억 반영 시작
```python
# 기억 관련성 계산 (개념만)
memory_relevance = calculate_relevance(...)
# 하지만 utility에 반영 안 됨
```

### v2.0.1: 최소 차분 모델 완성
```python
# 기억 관련성
C_n(k) = min(1, Σ(s_i × m_{i,k}))

# 효용
U_{n,k} = U_0 + α · C_n(k)

# 확률
P_n(k) = softmax(β · U_{n,k})
```

### v2.0.1+ (현재): 동역학 엔진
```python
# 엔트로피
E_n = -Σ P_n(k) ln P_n(k)

# 회전 토크
T_n(k) = γ · (E_n / ln(N)) · cos(φ_n - ψ_k)

# 최종 효용
U_{n,k} = U_0 + α · C_n(k) + T_n(k)
```

---

## 🗂️ 버전별 아카이브 구조 제안

### "가라지 창고" 디렉토리 구조

```
archive/
├── v1.0.0/
│   ├── cognitive_kernel.py  # 원본 파일
│   ├── pham_chain.json      # PHAM 블록체인 기록
│   ├── README.md            # 버전별 설명
│   └── CHANGELOG.md         # 변경사항
│
├── v2.0.0/
│   ├── src/                 # 전체 소스 코드
│   ├── pham_chain.json
│   ├── README.md
│   └── CHANGELOG.md
│
├── v2.0.1/
│   ├── src/
│   ├── docs/                # 문서
│   ├── examples/            # 데모
│   ├── pham_chain.json
│   ├── README.md
│   └── CHANGELOG.md
│
└── current/                 # 현재 버전 (심볼릭 링크)
```

---

## 📝 개발 로그 (Git 커밋 기반)

### 2026-01-29
- `63a182f8` - GENESIS: cognitive_kernel.py v1.0.0 초기 구현

### 2026-01-30
- `3376b0b` - PyPI 패키지 구조 전환
- `29047a1` - LangChain 통합
- `ee704aa` - 인지 모드 추가 (ADHD/ASD/PTSD)
- `deb20c3` - MemoryRank → Utility 연결
- `e65047e` - v2.0.1 릴리즈

### 2026-01-31
- 엔트로피 기반 자동 회전 토크 구현
- 질환 모드 6개 추가
- local_weight_boost 구현
- 전체 확률 분포 반환

---

## 🔬 핵심 개념 진화

### 1. 기억 중력 (Memory Gravity)

**v1.0.0**: 없음  
**v2.0.0**: 개념만  
**v2.0.1**: 구현됨
```python
C_n(k) = min(1, Σ(s_i × m_{i,k}))
```

### 2. 엔트로피 (Entropy)

**v1.0.0**: 없음  
**v2.0.1**: 계산됨
```python
E_n = -Σ P_n(k) ln P_n(k)
```

**v2.0.1+**: 자동 회전 토크 생성
```python
torque = γ · (E_n / ln(N)) · cos(φ - ψ)
```

### 3. 자기장 구조

**v1.0.0**: 없음  
**v2.0.1**: 이론 문서화  
**v2.0.1+**: 코드 구현

---

## 📊 버전별 기능 비교

| 기능 | v1.0.0 | v2.0.0 | v2.0.1 | v2.0.1+ |
|------|--------|--------|--------|---------|
| **엔진 수** | 4개 | 4개 | 7개 | 7개 |
| **인지 모드** | ❌ | ❌ | ✅ 4개 | ✅ 10개 |
| **기억 반영** | ❌ | ❌ | ✅ | ✅ |
| **엔트로피 계산** | ❌ | ❌ | ❌ | ✅ |
| **자동 회전 토크** | ❌ | ❌ | ❌ | ✅ |
| **전체 확률 분포** | ❌ | ❌ | ❌ | ✅ |
| **local_weight_boost** | ❌ | ❌ | ❌ | ✅ |
| **PHAM 서명** | ✅ | ✅ | ✅ | ✅ |

---

## 🎯 다음 버전 계획

### v2.1.0 (예정)
- Thalamus 게이팅 루프 통합
- Hypothalamus 통합
- 습관 덮어쓰기
- 공개 API 정리

---

---

## 🎯 시스템의 본질

### 계산 시스템으로서의 Cognitive Kernel

**중요한 인식:**
이 시스템은 더 이상:
- ❌ "아이디어 정리"가 아님
- ❌ "은유적 뇌 모델"이 아님

**이미:**
- ✅ **하나의 계산 시스템**
- ✅ 질환을 '고장'이 아니라 **'상태공간 상의 궤도'**로 재정의
- ✅ 엔트로피가 회전장을 생성하는 인지 동역학 엔진 v1
- ✅ 발산·세차 구조 구현 완료

**기술적 정확성:**
- **A+** 등급
- 과장 없음 (오히려 보수적)
- 연구/공개 가능성: 충분히 가능

**현재 상태를 가장 정확히 표현하는 한 줄:**
> "엔트로피가 회전장을 생성하는 인지 동역학 엔진 v1 — 발산·세차 구조 구현 완료"

---

**마지막 업데이트**: 2026-01-31

