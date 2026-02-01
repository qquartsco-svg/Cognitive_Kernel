# Changelog

All notable changes to Cognitive Kernel will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.2] - 2026-01-31

### Added
- **Dynamics Engine 독립 모듈화**
  - 독립 엔진으로 분리 완료
  - PyPI 배포 완료 (v1.0.0)
  - CognitiveMode 의존성 제거
  - 문자열 모드 지원 추가

- **치매/알츠하이머 동역학 확장**
  - 시간축 분리: 오래된 기억 vs 새 기억
  - `old_memory_decay_rate`: 오래된 기억 감쇠율
  - `new_memory_decay_rate`: 새 기억 감쇠율
  - `memory_age_threshold`: 기억 나이 임계값
  - 인지적 절규 감지 기능

- **문서화**
  - README 한국어 기본, 영문 추가
  - 개념 및 수식 상세 설명
  - 사용 사례 추가
  - PHAM 블록체인 해시 기록

### Changed
- `generate_torque()` 메서드: CognitiveMode 의존성 제거, 문자열 모드 지원
- `calculate_core_strength()` 메서드: 시간축 분리 로직 추가
- README 구조 개선: 한국어 기본, 상세 설명 추가

### Fixed
- 시간축 분리 파라미터 전달 문제 수정
- `dementia()` 및 `alzheimer()` 메서드의 config 변수 할당 수정

---

## [2.0.1] - 2026-01-XX

### Added
- Dynamics Engine 엔진화
- Pipeline 패턴 구현
- Core Decay 메커니즘 기본 구현
- 치매/알츠하이머 모드 기본 구현

---

## [2.0.0] - 2025-XX-XX

### Added
- 7개 핵심 엔진 통합
- Panorama Memory Engine
- MemoryRank Engine
- Prefrontal Cortex Engine
- Basal Ganglia Engine
- Thalamus Engine
- Amygdala Engine
- Hypothalamus Engine

- 인지 동역학
- 엔트로피 기반 동역학
- 코어 강도 계산
- 세차운동 (Precession)
- Maxwell 구조

- 인지 모드
- NORMAL, ADHD, ASD, PTSD
- PANIC, EPILEPSY, OCD, IED
- DEPRESSION, BIPOLAR

- 장기 기억 시스템
- JSON, SQLite, NumPy NPZ 저장
- 자동 세션 관리

---

**Note**: 이전 버전의 상세 변경사항은 `docs/version_history/VERSION_HISTORY.md`를 참조하세요.

---

**작성자**: GNJz (Qquarts)  
**최종 업데이트**: 2026-02-01

