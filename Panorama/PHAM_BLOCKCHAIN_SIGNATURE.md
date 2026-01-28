# PHAM Blockchain Signature

## Project Metadata

| 항목 | 값 |
|------|---|
| **Project Name** | Panorama Memory Engine |
| **Version** | v1.0.0 |
| **Author** | GNJz (Qquarts) |
| **Date** | 2025-01-28 |
| **License** | MIT |

---

## Technical Summary

**Panorama Memory Engine**은 시간축 기반 에피소드 기억 엔진입니다.

### 핵심 알고리즘

1. **Binary Search Insert/Query**: 시간 순 정렬된 이벤트 리스트에서 O(log n) 삽입 및 구간 쿼리
2. **Time Gap Segmentation**: 시간 간격 임계값 기반 에피소드 자동 분할
3. **Exponential Decay**: 지수 감쇠를 통한 최근성 기반 중요도 계산

### 수식

```
# 에피소드 분할 조건
new_episode if (t_i - t_{i-1}) > τ

# 지수 감쇠 중요도
importance(t) = base_importance × exp(-λ × Δt)
λ = ln(2) / half_life
```

---

## Cryptographic Proof

### File Hashes (SHA-256)

| 파일 | SHA-256 Hash |
|------|-------------|
| panorama_engine.py | 721ad07dd0ae6b6a59f9fb474c869b7fcc0ef0c067a25ef118cce13869496114 |
| config.py | 4b00506884f3f3e4aed56400aa5e5914310e3e6357d54ef2620ea69483ce0f8b |
| README.md | ec9da13c2a78d842fc985bd2dec5b04d0a2c44ef8c5d772e7f734186e90126b1 |

### PHAM Chain Record

| 항목 | 값 |
|------|---|
| Block Hash | (PHAM 체인 기록 후 업데이트) |
| PHAM Score | (PHAM 체인 기록 후 업데이트) |
| Timestamp | 2025-01-28T00:00:00Z |

---

## Verification

```bash
# 파일 무결성 검증
shasum -a 256 package/panorama/panorama_engine.py
# 예상: 721ad07dd0ae6b6a59f9fb474c869b7fcc0ef0c067a25ef118cce13869496114

shasum -a 256 package/panorama/config.py
# 예상: 4b00506884f3f3e4aed56400aa5e5914310e3e6357d54ef2620ea69483ce0f8b
```

---

## Signature

```
-----BEGIN PHAM SIGNATURE-----
Project: Panorama_Memory_Engine
Version: v1.0.0
Author: GNJz (Qquarts)
Hash: SHA256:721ad07dd0ae6b6a59f9fb474c869b7fcc0ef0c067a25ef118cce13869496114
Date: 2025-01-28
-----END PHAM SIGNATURE-----
```
