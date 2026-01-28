# PHAM BLOCKCHAIN SIGNATURE – MemoryRank Engine v1.0

- Project: Cookiie Brain – MemoryRank Engine
- Module: 11.MemoryRank_Engine
- Version: v1.0.0
- Author: GNJz (Qquarts)
- Date: 2025-01-28
- License: MIT

## Technical Summary

- Core Algorithm: **Google PageRank** (Brin & Page, 1998)
- Variant: Personalized PageRank with emotion/recency/frequency weights
- Domain: Memory / Knowledge Graph Ranking
- Intended Uses:
  - Industrial / Commercial: content ranking, search reranking, recommendation, log analysis
  - Research: brain disorder simulation (PTSD, depression, ADHD), cognitive modeling, network science

## Implementation Notes

- Engine Path: `package/memoryrank`
- Main Classes:
  - `MemoryRankConfig`
  - `MemoryNodeAttributes`
  - `MemoryRankEngine`
- Mathematical Definition:
  - r^{(t+1)} = α M r^{(t)} + (1 - α) v
  - where M is the column-normalized transition matrix and v is the personalization vector.

## Cryptographic Proof (PHAM v4 Signed)

### Source Files

| File | SHA-256 Hash | PHAM Score |
|------|--------------|------------|
| `memoryrank_engine.py` | `696d8760b66830bf5ea4a4b17880ddd30cf66922ddfe9418d037a277505f6840` | A_HIGH (0.9997) |
| `config.py` | (see pham_chain_config.json) | A_HIGH (0.9924) |
| `README.md` | `1d4a989393130013910e13542ef956584611d3bbe13f0c03a6a9e6b394ddfb3e` | A_HIGH (1.0000) |

### Block Hashes

| Chain File | Block Hash |
|------------|------------|
| `pham_chain_memoryrank_engine.json` | `79c6b43daf2750b2b7a9deed4f133a0d1975c705dd14e66219eeaa8fca12f5a6` |
| `pham_chain_README.json` | `7548ecb0c6d3ca9801c82fc3b64132c575c6725ad2f296e0fcf6e6db625f453f` |

### PHAM Chain Record

- Chain: `cookiie-brain-pham`
- Sign Tool: `pham_sign_v4.py`
- Signed Date: 2025-01-28

---

This signature certifies that the MemoryRank Engine v1.0 implementation
follows the specification based on Google PageRank and its personalized
variants, and that the above hashes correspond to the released
source code and documentation at the time of signing.
