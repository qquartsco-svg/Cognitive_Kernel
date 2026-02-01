# 최종 작업 로드맵: v2.0.2 → v2.1.0

**작성일**: 2026-02-01  
**기준**: 냉정한 피드백 및 코드 계약 분석 반영

---

## 📊 현재 상태 재평가

### 완료된 것
- ✅ Phase 1: 증거화 및 고정
- ✅ Phase 2: 프로젝트 정리 (부분)
- ✅ Dynamics Engine 독립화
- ✅ 치매/알츠하이머 파라미터 추가

### 부족한 것 (다음 작업의 정체)
1. **재현 가능한 벤치마크/검증** (Validation)
2. **API 안정성 + 호환성 보장** (Contract)
3. **사용자가 '바로 붙일' 통합 예제/레퍼런스 앱** (Reference Integration)

---

## 🎯 최종 우선순위 (4가지 관점 종합)

### 🔴 최우선: API 계약 고정 + 테스트 재편

**이유**: 모든 관점의 기반 작업

#### Phase 3-1: API 계약 고정 (4-6시간)

**목적**: "이 버전에서 이 함수는 이렇게 동작한다" 고정

**작업**:
1. 입력 스키마 명시 (1-2시간)
   - `remember()`: content, importance, metadata 타입/범위
   - `recall()`: k 범위, query 형식
   - `decide()`: options 타입, 빈 리스트 처리
   - `set_mode()`: 허용 모드 목록, 대소문자 정책

2. 출력 스키마 명시 (1-2시간)
   - `decide()`: 필수 키 (`action`, `probability_distribution`, `entropy`, `core_strength`)
   - `recall()`: 필수 필드 (`id`, `importance`, `timestamp`)
   - 빈 케이스 처리 (`{}`, `[]`)

3. 에러 처리 정책 (1-2시간)
   - 확률 합 != 1.0 처리 (정규화? 예외?)
   - timestamp 유효성 검사
   - importance 범위 검사 (0~1 강제?)
   - 예외 타입 정의

4. 계약 테스트 작성 (1-2시간)
   - 입력 스키마 검증 테스트
   - 출력 스키마 검증 테스트
   - 에러 케이스 테스트

**Deliverable**:
- `API_REFERENCE.md` (완전한 스펙)
- `tests/test_api_contract.py` (스펙 기반 테스트)

---

#### Phase 3-2: 테스트 재편 (커버리지 축 기준) (4-6시간)

**목적**: 파일 수가 아닌 커버리지 축으로 재편

**작업**:
1. 수학 축 테스트 (1-2시간)
   - entropy 단조성, 경계값 (0, lnN)
   - core_decay 연속성 (Δt=0, 큰 Δt)
   - persistent_core 업데이트

2. 상태 축 테스트 (1시간)
   - precession_phi wrap (0~2π)
   - history maxlen
   - 상태 초기화

3. 모드 축 테스트 (1-2시간)
   - normal/adhd/asd 문자열 모드
   - dementia/alzheimer 파라미터 차이
   - 모드 전환

4. 재현성 축 테스트 (1-2시간)
   - time mock
   - 고정 timestamp
   - 결정론적 테스트

5. 치매/알츠하이머 차이 명확화 (1시간)
   - old_memory vs new_memory 시간 경과
   - core_strength 변화 비교
   - "차이가 반드시 출력되는" 골든 테스트

**Deliverable**:
- `tests/test_mathematical_models.py` (확장)
- `tests/test_state_management.py`
- `tests/test_cognitive_modes.py`
- `tests/test_reproducibility.py`
- `tests/test_dementia_alzheimer_time_axis.py` (개선)

---

### 🟡 높음: 의료 표현 고정 + 레퍼런스 앱

#### Phase 3-3: 의료 표현 고정 (2-3시간)

**작업**:
1. Non-medical Disclaimer (1시간)
   - `MEDICAL_DISCLAIMER.md` 생성
   - README에 2-3줄 추가
   - 표현 고정 ("진단/예측" → "시뮬레이션")

2. 검증 지표 정의 (1시간)
   - 새 기억 유지율
   - 재호출 안정성
   - core_strength half-life

3. 윤리/오용 방지 (1시간)
   - `ETHICS_AND_SAFETY.md` 생성
   - 임상 의사결정 금지 명시

**Deliverable**:
- `MEDICAL_DISCLAIMER.md`
- `VALIDATION_METRICS.md`
- `ETHICS_AND_SAFETY.md`

---

#### Phase 3-4: 레퍼런스 앱 1개 (2-3시간)

**작업**:
- 고객지원 챗봇 예제
- 또는 개발자 코파일럿 예제
- 30초 데모 가능한 형태

**Deliverable**:
- `examples/reference_app/`

---

### 🟢 중간: 산업용 통합 + 상업용 포지셔닝

#### Phase 3-5: 산업용 통합 레이어 (6-8시간)

**작업**:
1. 통합 어댑터 예제 (3-4시간)
   - LangChain 어댑터
   - 저장소 백엔드 옵션

2. 성능 벤치마크 (2-3시간)
   - N=1e5 성능 테스트
   - 메모리 프로파일링

3. 운영 문서 (1-2시간)
   - `UPGRADE_GUIDE.md`
   - `TUNING_GUIDE.md`

**Deliverable**:
- `examples/agent_memory_adapter/`
- `PERFORMANCE.md`
- `UPGRADE_GUIDE.md`, `TUNING_GUIDE.md`

---

#### Phase 3-6: 상업용 포지셔닝 (4-6시간)

**작업**:
1. 1줄 가치 재정의 (1시간)
   - README 상단 5줄 재작성
   - 실사용 케이스 중심

2. 라이선스/패키징 문서 (1-2시간)
   - `SUPPORT.md`
   - `SECURITY.md`
   - `ROADMAP.md`

**Deliverable**:
- `README.md` (상단 수정)
- `SUPPORT.md`, `SECURITY.md`, `ROADMAP.md`

---

## 📅 상세 일정

### Day 1-2: API 계약 고정 (최우선)

**Day 1 (4-6시간)**:
- 오전: 입력/출력 스키마 명시
- 오후: 에러 처리 정책 + 계약 테스트

**Day 2 (4-6시간)**:
- 테스트 재편 (커버리지 축)
- 치매/알츠하이머 차이 명확화

---

### Day 3: 의료 표현 + 레퍼런스 앱

**Day 3 (4-6시간)**:
- 오전: 의료 표현 고정
- 오후: 레퍼런스 앱 1개

---

### Day 4-5: 산업용 + 상업용

**Day 4 (6-8시간)**: 산업용 통합 레이어  
**Day 5 (4-6시간)**: 상업용 포지셔닝

---

## ✅ 완료 기준

### v2.1.0 릴리스 기준

1. **API 계약 고정**
   - ✅ 입력/출력 스키마 명시
   - ✅ 에러 처리 정책 수립
   - ✅ 계약 테스트 통과

2. **테스트 재편**
   - ✅ 커버리지 축 기준 테스트 완성
   - ✅ 치매/알츠하이머 차이 명확화

3. **의료 표현 고정**
   - ✅ Non-medical disclaimer
   - ✅ 검증 지표 정의

4. **레퍼런스 앱**
   - ✅ 30초 데모 가능한 예제 1개

---

## ⚠️ 작업 원칙 (재확인)

### ✅ 반드시 해야 할 것
1. API 계약 고정 (최우선)
2. 테스트 재편 (커버리지 축)
3. 레퍼런스 앱 1개

### ❌ 절대 하지 말 것
1. 기능 추가
2. 엔진 더 만들기
3. 개념 문서 추가
4. 설명 보강

---

**작성자**: GNJz (Qquarts)  
**최종 업데이트**: 2026-02-01  
**상태**: 코드 계약 분석 완료, 실행 준비

