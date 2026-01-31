# 🔗 PHAM 블록체인 기록 로그

> **블록체인 해시 순서대로 정리된 개발 기록**

**작성일**: 2026-01-31  
**현재 버전**: v2.0.1+

---

## 🎯 목적

PHAM 블록체인에 기록된 모든 모듈의 해시와 TxID를 순서대로 정리하여:
- 개발 과정 추적
- 버전별 변화 확인
- 블록체인 무결성 검증
- 과거 버전 복구

---

## 📋 메인 체인: Cognitive Kernel

### GENESIS 블록

```json
{
  "index": 0,
  "timestamp": 1769618026.868311,
  "data": {
    "name": "GENESIS"
  },
  "hash": "0"
}
```

---

### 블록 1: cognitive_kernel.py v1.0.0

**파일**: `pham_chain_cognitive_kernel.json`

```json
{
  "index": 1,
  "timestamp": 1769618026.868313,
  "data": {
    "title": "cognitive_kernel.py",
    "author": "GNJz",
    "timestamp": "2026-01-29 03:33:46",
    "hash": "63a182f8a1420231ee3d45efd5d0b9d2800be6790619934f8f2f82daf3e57454",
    "cid": "Qme2rgSYgFzmNszMVV5eMu9ShV7uMLCn8Uj26J9XeosCe9",
    "description": "CognitiveKernel v1.0 - 통합 인지 엔진, 자동 세션 관리, 진짜 장기 기억",
    "score": 0.9998,
    "label": "A_HIGH"
  },
  "previous_hash": "0",
  "hash": "f4261fd69f4146391caec7da3ea46b2961dee50e8724ea2f72c4139e1c8de357"
}
```

**특징:**
- **해시**: `63a182f8a1420231ee3d45efd5d0b9d2800be6790619934f8f2f82daf3e57454`
- **IPFS CID**: `Qme2rgSYgFzmNszMVV5eMu9ShV7uMLCn8Uj26J9XeosCe9`
- **점수**: 0.9998 (A_HIGH)
- **내용**: v1.0.0 초기 구현

**주요 기능:**
- 통합 인지 엔진
- 자동 세션 관리
- 4개 엔진 통합 (Panorama, MemoryRank, PFC, BasalGanglia)
- 장기 기억 저장/로드

---

## 🔧 엔진별 PHAM 체인

### 1. MemoryRank Engine

**파일들:**
- `MemoryRank/pham_chain_memoryrank_engine.json`
- `MemoryRank/pham_chain_config.json`
- `MemoryRank/pham_chain_README.json`
- `src/cognitive_kernel/engines/memoryrank/pham_chain_persistence.json`

**기록 내용:**
- MemoryRank 알고리즘 구현
- PageRank 기반 중요도 계산
- 그래프 구축 및 랭킹

---

### 2. Panorama Engine

**파일들:**
- `Panorama/package/panorama/pham_chain_persistence.json`
- `src/cognitive_kernel/engines/panorama/pham_chain_persistence.json`

**기록 내용:**
- 시간축 기억 저장
- 이벤트 타임라인 관리
- Recency 점수 계산

---

### 3. BasalGanglia Engine

**파일들:**
- `BasalGanglia/blockchain/pham_chain_basal_ganglia_engine.json`
- `BasalGanglia/blockchain/pham_chain_config.json`
- `BasalGanglia/blockchain/pham_chain_data_types.json`

**기록 내용:**
- Q-Learning 기반 습관 학습
- 보상 학습 알고리즘
- 컨텍스트-행동 매핑

---

## 📊 블록체인 체인 구조

```
GENESIS (hash: "0")
    ↓
cognitive_kernel.py v1.0.0
    Hash: 63a182f8a1420231ee3d45efd5d0b9d2800be6790619934f8f2f82daf3e57454
    CID: Qme2rgSYgFzmNszMVV5eMu9ShV7uMLCn8Uj26J9XeosCe9
    Previous Hash: 0
    Block Hash: f4261fd69f4146391caec7da3ea46b2961dee50e8724ea2f72c4139e1c8de357
    ↓
    [다음 버전 블록들...]
```

---

## 🔍 해시 검증 방법

### 1. 파일 해시 계산

```bash
# SHA-256 해시 계산
sha256sum cognitive_kernel.py
```

### 2. 블록체인 무결성 검증

```python
import hashlib
import json

def verify_block(block):
    """블록 해시 검증"""
    # previous_hash와 data를 합쳐서 해시 계산
    data_str = json.dumps(block["data"], sort_keys=True)
    combined = block["previous_hash"] + data_str
    calculated_hash = hashlib.sha256(combined.encode()).hexdigest()
    
    return calculated_hash == block["hash"]
```

---

## 📝 버전별 PHAM 기록

### v1.0.0 (2026-01-29)

**블록 정보:**
- Index: 1
- Hash: `63a182f8a1420231ee3d45efd5d0b9d2800be6790619934f8f2f82daf3e57454`
- CID: `Qme2rgSYgFzmNszMVV5eMu9ShV7uMLCn8Uj26J9XeosCe9`
- Score: 0.9998
- Label: A_HIGH

**파일:**
- `cognitive_kernel.py` (단일 파일)

---

### v2.0.0 (2026-01-30)

**Git 커밋:**
- `3376b0b` - feat: Add PyPI package structure (v2.0.0)

**변경사항:**
- PyPI 패키지 구조로 전환
- `src/cognitive_kernel/` 구조

**PHAM 기록:**
- 각 엔진 모듈별 독립적인 PHAM 체인 생성

---

### v2.0.1 (2026-01-30 ~ 2026-01-31)

**Git 커밋:**
- `ee704aa` - feat: Add Cognitive Modes (ADHD/ASD/PTSD)
- `deb20c3` - feat: MemoryRank → Action Utility 연결 구현
- `e65047e` - chore: v2.0.1 버전 업데이트 및 릴리즈 노트

**변경사항:**
- 인지 모드 추가
- 기억 기반 의사결정 구현
- 엔트로피 기반 자동 회전 토크

**PHAM 기록:**
- 각 엔진 모듈 업데이트 시 PHAM 체인에 기록
- 버전별 해시 추적

---

## 🗂️ PHAM 파일 위치

### 메인 체인
- `/pham_chain_cognitive_kernel.json`

### 엔진별 체인
- `/MemoryRank/pham_chain_memoryrank_engine.json`
- `/MemoryRank/pham_chain_config.json`
- `/MemoryRank/pham_chain_README.json`
- `/MemoryRank/package/memoryrank/pham_chain_persistence.json`
- `/Panorama/package/panorama/pham_chain_persistence.json`
- `/BasalGanglia/blockchain/pham_chain_basal_ganglia_engine.json`
- `/BasalGanglia/blockchain/pham_chain_config.json`
- `/BasalGanglia/blockchain/pham_chain_data_types.json`
- `/src/cognitive_kernel/engines/memoryrank/pham_chain_persistence.json`
- `/src/cognitive_kernel/engines/panorama/pham_chain_persistence.json`

---

## 🔐 PHAM 서명 프로세스

### 1. 파일 해시 계산
```python
import hashlib

def calculate_file_hash(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
    return hashlib.sha256(content).hexdigest()
```

### 2. 블록 생성
```python
def create_block(data, previous_hash):
    block = {
        "index": len(chain) + 1,
        "timestamp": time.time(),
        "data": data,
        "previous_hash": previous_hash,
    }
    block["hash"] = calculate_block_hash(block)
    return block
```

### 3. 체인에 추가
```python
def add_block_to_chain(block):
    chain.append(block)
    save_chain_to_json(chain, "pham_chain.json")
```

---

## 📈 버전별 해시 추적

| 버전 | 파일 | 해시 | CID | 점수 |
|------|------|------|-----|------|
| v1.0.0 | cognitive_kernel.py | `63a182f8...` | `Qme2rg...` | 0.9998 |
| v2.0.0 | src/cognitive_kernel/core.py | (Git 커밋) | - | - |
| v2.0.1 | src/cognitive_kernel/core.py | (Git 커밋) | - | - |

---

## 🎯 다음 단계

### PHAM 서명 필요 모듈

다음 버전 업데이트 시 PHAM 서명이 필요한 모듈:

1. **MemoryRank Engine**
   - `local_weight_boost` 구현 완료
   - PHAM 서명 필요

2. **Cognitive Modes**
   - 6개 질환 모드 추가 완료
   - PHAM 서명 필요

3. **Core Engine**
   - 엔트로피 기반 자동 회전 토크 구현
   - PHAM 서명 필요

---

## 📝 PHAM 서명 체크리스트

버전 업데이트 전:

- [ ] 모든 변경된 파일 해시 계산
- [ ] 블록체인 블록 생성
- [ ] IPFS CID 생성
- [ ] PHAM 체인에 추가
- [ ] 해시 검증
- [ ] 문서 업데이트

---

**마지막 업데이트**: 2026-01-31

