# 🔗 PHAM 블록체인 서명 정보

## 📋 개요

이 Basal Ganglia Engine은 **PHAM (Proof of Authorship & Merit) 블록체인 시스템**으로 서명되어 있습니다.

### PHAM 블록체인이란?

PHAM은 코드 기여도를 추적하고 보상하는 블록체인 시스템입니다:

1. **작성자 증명 (Proof of Authorship)**: 코드 작성자를 블록체인에 기록
2. **기여도 추적 (Merit Tracking)**: 코드 변경 사항의 기여도를 4-Signal Scoring으로 계산
3. **수익 분배 (Revenue Sharing)**: 기여도에 따라 수익을 자동 분배
4. **IPFS 통합**: 코드 버전을 IPFS에 저장하여 영구 보존

---

## 🔐 4-Signal Scoring 시스템

각 코드 변경은 다음 4가지 신호로 평가됩니다:

| 신호 | 가중치 | 설명 |
|------|--------|------|
| **Byte Signal** | 25% | 바이트 레벨 변경 비율 |
| **Text Signal** | 35% | 텍스트 유사도 (difflib) |
| **AST Signal** | 30% | AST 구조 변경 분석 |
| **Exec Signal** | 10% | 실행 결과 변화 |

**총점 = (Byte × 0.25) + (Text × 0.35) + (AST × 0.30) + (Exec × 0.10)**

---

## 💰 블록체인 기반 기여도 시스템

### 📌 기본 원칙

**라이선스**: 오픈소스 (MIT License)  
**사용 제한**: 없음  
**로열티 요구**: 없음

**수익 발생 시 기여도 시스템**:
- 코드 기여도: 코드 작성, 기능 추가, 버그 수정 등 (블록체인으로 계산됩니다)
- 제품 기여도: 상용화 과정 전반에 대한 기여 (블록체인으로 기록됩니다)
  - 제품화 및 상용화
  - 홍보 및 마케팅
  - 판매 및 배포
  - 기타 제품 성공에 기여한 모든 활동
- 기여도 합산: 모든 기여 활동이 블록체인에 기록되어 투명하게 합산됩니다
- 자동 분배: 블록체인으로 계산된 기여도에 따라 수익이 자동으로 분배됩니다

### 🔄 업그레이드 가능한 구조

블록체인 기반 기여도 시스템은 업그레이드 가능한 구조로, 현재는 초기 설계 단계이며 실제 상용화 경험을 통해 발전할 예정입니다. 구체적인 기여도 계산 방식이나 분배 메커니즘은 향후 커뮤니티와의 협의를 통해 결정됩니다.

### ⚠️ GNJz의 기여도 원칙 (블록체인 기반)

**최초 코드 작성자 GNJz (Qquarts)의 기여도는 블록체인으로 계산된 결과, 총 기여도 중 최대 6%를 넘지 않습니다.**

**블록체인 기반 신뢰 시스템 원칙**:
- 코드 재사용: 로열티 요구 없음, 자유롭게 사용 가능
- 수익 발생 시: 블록체인으로 계산된 기여도에 따라 수익 분배
- 기여도 계산: PHAM 블록체인의 4-Signal Scoring으로 객관적 계산
- GNJz의 자발적 제한: 기여도가 6%를 넘지 않도록 스스로 제한
- 검증 가능성: 블록체인으로 검증 가능한 기여도 상한선
- 투명성: 모든 기여도 계산은 블록체인에 기록되어 검증 가능

이 원칙은 코드가 어떻게 상용화되든, 누가 상용화하든 관계없이 블록체인에 영구 기록됩니다.

---

## 📁 블록체인 체인 파일

각 파일의 변경 이력은 다음 파일에 저장됩니다:

- `blockchain/pham_chain_basal_ganglia_engine.json` - 핵심 엔진 파일
- `blockchain/pham_chain_config.json` - 설정 파일
- `blockchain/pham_chain_data_types.json` - 데이터 타입
- `blockchain/pham_chain_readme.json` - README 문서

### 블록 구조

```json
{
  "index": 0,
  "timestamp": 1234567890.123,
  "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000",
  "data": {
    "title": "basal_ganglia_engine.py",
    "hash": "abc123...",
    "author": "GNJz",
    "description": "Basal Ganglia Engine 초기 구현",
    "signals": {
      "byte": 0.85,
      "text": 0.90,
      "ast": 0.80,
      "exec": 0.75
    },
    "score": 0.83,
    "label": "MAJOR",
    "raw_bytes": "hex_encoded_bytes...",
    "raw_text": "file_content...",
    "ipfs_cid": "QmXXX..."
  },
  "hash": "block_hash..."
}
```

---

## 🚀 사용 방법

### 1. 파일 서명

```bash
cd /Users/jazzin/Desktop/00_BRAIN/cookiie_brain/blockchain

# Basal Ganglia Engine 서명
python3 pham_sign_v4.py \
    ../../9.Basal_Ganglia_Engine/package/basal_ganglia/basal_ganglia_engine.py \
    --author "GNJz" \
    --desc "Basal Ganglia Engine 초기 구현" \
    --exec "python3 -m pytest ../../9.Basal_Ganglia_Engine/tests/ -v"
```

### 2. 블록체인 체인 확인

```bash
cat blockchain/pham_chain_basal_ganglia_engine.json | jq '.'
```

### 3. 기여도 확인

```bash
python3 pham_sign_v4.py --stats blockchain/pham_chain_basal_ganglia_engine.json
```

---

## ⚠️ 중요 사항

1. **모든 코드 변경은 블록체인에 기록됩니다**
   - 실수로 잘못된 코드를 커밋해도 이력이 남습니다
   - 신중하게 코드를 작성하고 테스트하세요

2. **🚫 스팸 필터링 시스템 (중요)**
   
   **의미없는 코드 수정은 기여도 계산에서 자동으로 제외됩니다.**
   
   PHAM 시스템은 다음과 같은 다층 필터링을 통해 의미있는 변경만 평가합니다:
   
   - **MIN_BYTE_CHANGE = 0.002 (0.2%)**: 
     - 바이트 변경이 0.2% 미만이면 의심으로 분류
     - 예: 변수명 하나만 바꾸고 해시 기록 남기는 경우
   
   - **THRESHOLD_LOW = 0.12 (12%)**: 
     - 4-Signal Scoring 결과가 12% 미만이면 **SPAM**으로 분류
     - SPAM으로 분류된 변경은 **기여도 계산에서 완전히 제외**됩니다
     - 수익 분배 시에도 합산되지 않습니다
   
   - **4-Signal Scoring 검증**:
     - Byte, Text, AST, Exec 4가지 신호를 종합 평가
     - 단순 변수명 변경은 AST/Exec 신호가 거의 0이므로 낮은 점수
     - 의미있는 기능 추가/수정만 높은 점수를 받습니다
   
   **결과**: 단순히 이름 하나 바꾸고 해시 기록 남기는 것 같은 의미없는 수정은 자동으로 필터링되어 기여도에 합산되지 않습니다.

3. **IPFS 저장**
   - 모든 코드 버전은 IPFS에 저장되어 영구 보존됩니다
   - IPFS CID를 통해 언제든지 이전 버전을 복원할 수 있습니다

4. **수익 분배**
   - `--pay` 옵션을 사용하면 블록체인 보상이 자동으로 지급됩니다
   - Web3 연결이 필요합니다

---

## 📞 문의

블록체인 관련 문의사항이 있으시면:
- GitHub Issues: [Repository URL]
- Email: [Contact Email]

---

**작성일**: 2025-01-25  
**버전**: 1.0.0-alpha  
**작성자**: GNJz (Qquarts)

