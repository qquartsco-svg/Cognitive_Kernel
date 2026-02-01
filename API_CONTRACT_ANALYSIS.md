# API 계약 분석 및 로드맵

**작성일**: 2026-02-01  
**목적**: 코드 간 계약 확인 및 정확한 로드맵 수립

---

## 🔍 현재 API 계약 상태 분석

### 1. 입력 스키마 확인 필요

#### remember()
- **현재**: `remember(content, importance=0.5, metadata=None)`
- **확인 필요**:
  - [ ] `content` 타입 (str만? dict도?)
  - [ ] `importance` 범위 (0~1 강제? 음수 허용?)
  - [ ] `metadata` 구조 (dict? None?)
  - [ ] `timestamp` 자동 생성? 수동 입력 가능?

#### recall()
- **현재**: `recall(k=10, query=None)`
- **확인 필요**:
  - [ ] `k` 범위 (최소/최대?)
  - [ ] `query` 형식 (str? dict?)
  - [ ] 빈 결과 처리 ([]? None?)

#### decide()
- **현재**: `decide(options, context=None)`
- **확인 필요**:
  - [ ] `options` 타입 (list만? dict도?)
  - [ ] `options` 빈 리스트 처리
  - [ ] `context` 구조

#### set_mode()
- **현재**: `set_mode(mode)`
- **확인 필요**:
  - [ ] 허용 모드 목록
  - [ ] 대소문자 정책
  - [ ] unknown 모드 처리

---

### 2. 출력 스키마 확인 필요

#### decide() 반환값
- **현재**: dict 형태
- **확인 필요**:
  - [ ] 필수 키: `action`, `probability_distribution`, `entropy`, `core_strength`?
  - [ ] 선택 키: `distress`, `torque`, `precession_phi`?
  - [ ] 빈 확률분포 `{}` 처리
  - [ ] 확률 합이 1.0이 아닌 경우

#### recall() 반환값
- **현재**: list of dict
- **확인 필요**:
  - [ ] 필수 필드: `id`, `importance`, `timestamp`?
  - [ ] 선택 필드: `content`, `metadata`?
  - [ ] 빈 리스트 `[]` vs `None`

---

### 3. 에러 처리 정책 확인 필요

- [ ] 확률 합이 1.0이 아닌 경우 (정규화? 예외?)
- [ ] `timestamp` 미래값/None 처리
- [ ] `importance` 범위 벗어남 (0~1 강제?)
- [ ] `options` 빈 리스트
- [ ] 메모리 부족 상황

---

## 📋 정확한 작업 로드맵

### Phase 3-1: API 계약 고정 (우선순위: 최우선)

**예상 시간**: 4-6시간  
**목적**: "이 버전에서 이 함수는 이렇게 동작한다" 고정

#### 작업 1.1: 입력 스키마 명시 (1-2시간)
- [ ] `remember()` 입력 스키마 문서화
- [ ] `recall()` 입력 스키마 문서화
- [ ] `decide()` 입력 스키마 문서화
- [ ] `set_mode()` 허용 모드 목록 고정

**Deliverable**: `API_REFERENCE.md` (입력 스키마 섹션)

#### 작업 1.2: 출력 스키마 명시 (1-2시간)
- [ ] `decide()` 반환값 구조 명시
- [ ] `recall()` 반환값 구조 명시
- [ ] 빈 케이스 처리 명시
- [ ] 예외 케이스 명시

**Deliverable**: `API_REFERENCE.md` (출력 스키마 섹션)

#### 작업 1.3: 에러 처리 정책 수립 (1-2시간)
- [ ] 확률 합 != 1.0 처리 정책
- [ ] timestamp 유효성 검사
- [ ] importance 범위 검사
- [ ] 예외 타입 정의

**Deliverable**: `API_REFERENCE.md` (에러 처리 섹션) + 코드 수정

#### 작업 1.4: 계약 테스트 작성 (1-2시간)
- [ ] 입력 스키마 검증 테스트
- [ ] 출력 스키마 검증 테스트
- [ ] 에러 케이스 테스트
- [ ] 스펙 기반 테스트

**Deliverable**: `tests/test_api_contract.py`

---

### Phase 3-2: 테스트 재편 (커버리지 축 기준)

**예상 시간**: 4-6시간  
**목적**: 파일 수가 아닌 커버리지 축으로 재편

#### 작업 2.1: 수학 축 테스트 (1-2시간)
- [ ] entropy 단조성 테스트
- [ ] entropy 경계값 테스트 (0, lnN)
- [ ] core_decay 연속성 테스트 (Δt=0, 큰 Δt)
- [ ] persistent_core 업데이트 테스트

**Deliverable**: `tests/test_mathematical_models.py` (확장)

#### 작업 2.2: 상태 축 테스트 (1시간)
- [ ] precession_phi wrap 테스트 (0~2π)
- [ ] history maxlen 테스트
- [ ] 상태 초기화 테스트

**Deliverable**: `tests/test_state_management.py`

#### 작업 2.3: 모드 축 테스트 (1-2시간)
- [ ] normal/adhd/asd 문자열 모드 테스트
- [ ] dementia/alzheimer 파라미터 차이 테스트
- [ ] 모드 전환 테스트

**Deliverable**: `tests/test_cognitive_modes.py`

#### 작업 2.4: 재현성 축 테스트 (1-2시간)
- [ ] time mock 테스트
- [ ] 고정 timestamp 테스트
- [ ] 결정론적 테스트 (같은 입력 → 같은 출력)

**Deliverable**: `tests/test_reproducibility.py`

#### 작업 2.5: 치매/알츠하이머 차이 명확화 테스트 (1시간)
- [ ] old_memory vs new_memory 시간 경과 테스트
- [ ] core_strength 변화 비교 테스트
- [ ] "차이가 반드시 출력되는" 골든 테스트

**Deliverable**: `tests/test_dementia_alzheimer_time_axis.py` (개선)

---

### Phase 3-3: 의료 표현 고정

**예상 시간**: 2-3시간

#### 작업 3.1: Non-medical Disclaimer (1시간)
- [ ] MEDICAL_DISCLAIMER.md 생성
- [ ] README에 2-3줄 추가
- [ ] 표현 고정 ("진단/예측" → "시뮬레이션")

**Deliverable**: `MEDICAL_DISCLAIMER.md`

#### 작업 3.2: 검증 지표 정의 (1시간)
- [ ] 새 기억 유지율 지표
- [ ] 재호출 안정성 지표
- [ ] core_strength half-life 지표

**Deliverable**: `VALIDATION_METRICS.md`

#### 작업 3.3: 윤리/오용 방지 (1시간)
- [ ] ETHICS_AND_SAFETY.md 생성
- [ ] 임상 의사결정 금지 명시
- [ ] 개인 정보 주의사항

**Deliverable**: `ETHICS_AND_SAFETY.md`

---

### Phase 3-4: 산업용 통합 레이어

**예상 시간**: 6-8시간

#### 작업 4.1: 통합 어댑터 예제 (3-4시간)
- [ ] LangChain 어댑터 예제
- [ ] REST API 예제 (선택적)
- [ ] 저장소 백엔드 옵션 (json/sqlite)

**Deliverable**: `examples/agent_memory_adapter/`

#### 작업 4.2: 성능 벤치마크 (2-3시간)
- [ ] N=1e5 근처 성능 테스트
- [ ] 메모리 사용량 프로파일링
- [ ] 계산 비용 측정

**Deliverable**: `PERFORMANCE.md` + 벤치마크 스크립트

#### 작업 4.3: 운영 문서 (1-2시간)
- [ ] UPGRADE_GUIDE.md
- [ ] TUNING_GUIDE.md
- [ ] 버전 정책 명시

**Deliverable**: `UPGRADE_GUIDE.md`, `TUNING_GUIDE.md`

---

### Phase 3-5: 상업용 포지셔닝

**예상 시간**: 4-6시간

#### 작업 5.1: 1줄 가치 재정의 (1시간)
- [ ] README 상단 5줄 재작성
- [ ] 실사용 케이스 중심
- [ ] 기술 용어 최소화

**Deliverable**: `README.md` (상단 수정)

#### 작업 5.2: 레퍼런스 앱 1개 (2-3시간)
- [ ] 고객지원 챗봇 예제
- [ ] 또는 개발자 코파일럿 예제
- [ ] 30초 데모 가능한 형태

**Deliverable**: `examples/reference_app/`

#### 작업 5.3: 라이선스/패키징 문서 (1-2시간)
- [ ] SUPPORT.md
- [ ] SECURITY.md (보안 정책)
- [ ] ROADMAP.md (짧게)

**Deliverable**: `SUPPORT.md`, `SECURITY.md`, `ROADMAP.md`

---

## 📅 우선순위별 일정

### 즉시 시작 (Day 1-2): API 계약 고정

**Day 1 (4-6시간)**:
- 오전: 입력/출력 스키마 명시
- 오후: 에러 처리 정책 + 계약 테스트

**목표**: API Contract 완전 고정

---

### 단기 (Day 3-4): 테스트 재편

**Day 3 (4-6시간)**:
- 수학/상태/모드/재현성 축 테스트
- 치매/알츠하이머 차이 명확화

**목표**: 커버리지 축 기준 테스트 완성

---

### 중기 (Day 5-7): 의료/산업/상업

**Day 5 (2-3시간)**: 의료 표현 고정  
**Day 6 (6-8시간)**: 산업용 통합 레이어  
**Day 7 (4-6시간)**: 상업용 포지셔닝

---

## 🎯 최종 우선순위

### 최우선 (즉시 시작)

1. **API 계약 고정** (4-6시간)
   - 입력/출력 스키마 명시
   - 에러 처리 정책
   - 계약 테스트

2. **테스트 재편** (4-6시간)
   - 커버리지 축 기준
   - 치매/알츠하이머 차이 명확화

### 높음 (단기)

3. **의료 표현 고정** (2-3시간)
4. **레퍼런스 앱 1개** (2-3시간)

### 중간 (중기)

5. **산업용 통합 레이어** (6-8시간)
6. **성능 벤치마크** (2-3시간)
7. **운영 문서** (1-2시간)

---

**작성자**: GNJz (Qquarts)  
**최종 업데이트**: 2026-02-01

