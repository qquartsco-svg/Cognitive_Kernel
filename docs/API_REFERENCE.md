# API Reference

**버전**: 2.0.2  
**작성일**: 2026-02-01  
**목적**: 산업용/연구용 기준 API 계약 명시

---

## 목차

1. [입력 스키마](#입력-스키마)
2. [출력 스키마](#출력-스키마)
3. [에러 처리](#에러-처리)
4. [예외 타입](#예외-타입)

---

## 입력 스키마

### `remember()`

기억 저장 (장기 기억)

#### 시그니처

```python
def remember(
    self,
    event_type: str,
    content: Optional[Dict[str, Any]] = None,
    importance: float = 0.5,
    emotion: float = 0.0,
    related_to: Optional[List[str]] = None,
) -> str
```

#### 파라미터

| 파라미터 | 타입 | 제약 | 기본값 | 설명 |
|---------|------|------|-------|------|
| `event_type` | `str` | 비어있지 않은 문자열 | - | 이벤트 종류 (예: "meeting", "idea") |
| `content` | `Optional[Dict[str, Any]]` | None 또는 dict | `None` | 이벤트 내용 |
| `importance` | `float` | 0.0 ~ 1.0 (포함) | `0.5` | 중요도 |
| `emotion` | `float` | 0.0 ~ 1.0 (포함) | `0.0` | 감정 강도 |
| `related_to` | `Optional[List[str]]` | None 또는 문자열 리스트 | `None` | 연관된 기억 ID 리스트 |

#### 반환값

- **타입**: `str`
- **형식**: UUID 문자열
- **설명**: 생성된 기억 ID

#### 예외

- `ValidationError`: 입력 검증 실패 시

#### 예제

```python
# 기본 사용
event_id = kernel.remember("meeting", {"topic": "project"}, importance=0.9)

# 연관 기억 포함
event_id = kernel.remember(
    "idea",
    {"content": "new feature"},
    importance=0.8,
    related_to=["id1", "id2"]
)
```

---

### `recall()`

중요한 기억 회상 (Top-k)

#### 시그니처

```python
def recall(self, k: int = 5) -> List[Dict[str, Any]]
```

#### 파라미터

| 파라미터 | 타입 | 제약 | 기본값 | 설명 |
|---------|------|------|-------|------|
| `k` | `int` | 양의 정수 (1 이상) | `5` | 회상할 기억 수 |

#### 반환값

- **타입**: `List[Dict[str, Any]]`
- **형식**: 중요도 순으로 정렬된 기억 리스트
- **필수 필드**:
  - `id`: `str` (기억 ID, UUID)
  - `event_type`: `str` (이벤트 종류)
  - `content`: `Dict[str, Any]` (이벤트 내용)
  - `importance`: `float` (중요도, 0.0 ~ 1.0)
  - `timestamp`: `float` (Unix timestamp)
- **빈 결과**: 기억이 없는 경우 빈 리스트 `[]` 반환

#### 예외

- `ValidationError`: k가 유효하지 않은 경우

#### 예제

```python
memories = kernel.recall(k=5)
for m in memories:
    print(f"{m['event_type']}: {m['importance']:.2f}")
```

---

### `decide()`

의사결정 (PFC + BasalGanglia)

#### 시그니처

```python
def decide(
    self,
    options: List[str],
    context: Optional[str] = None,
    use_habit: bool = True,
    external_torque: Optional[Dict[str, float]] = None,
    use_pipeline: bool = True,
) -> Dict[str, Any]
```

#### 파라미터

| 파라미터 | 타입 | 제약 | 기본값 | 설명 |
|---------|------|------|-------|------|
| `options` | `List[str]` | 비어있지 않은 문자열 리스트 | - | 행동 후보 리스트 |
| `context` | `Optional[str]` | None 또는 문자열 | `None` | 상황 컨텍스트 |
| `use_habit` | `bool` | - | `True` | 습관 학습 결과 반영 여부 |
| `external_torque` | `Optional[Dict[str, float]]` | None 또는 {option: value} | `None` | 외부 토크 값 |
| `use_pipeline` | `bool` | - | `True` | 파이프라인 패턴 사용 여부 |

#### 반환값

- **타입**: `Dict[str, Any]`
- **필수 키**:
  - `action`: `Optional[str]` (선택된 행동, None 가능)
  - `utility`: `float` (선택된 행동의 utility)
  - `probability`: `float` (선택된 행동의 확률)
  - `probability_distribution`: `Dict[str, float]` (모든 옵션의 확률 분포)
  - `entropy`: `float` (선택 불확실성, 엔트로피)
  - `core_strength`: `float` (코어 강도, 0.0 ~ 1.0)
- **선택 키**:
  - `habit_suggestion`: `Optional[str]` (습관 제안, None 가능)
  - `conflict`: `bool` (갈등 여부)
  - `cognitive_distress`: `bool` (인지적 고통 여부)
  - `distress_message`: `str` (고통 메시지)

#### 확률 분포 정규화

- `probability_distribution`의 모든 값의 합은 항상 1.0입니다.
- 정규화는 내부적으로 자동 수행됩니다.

#### 예외

- `ValidationError`: options가 유효하지 않은 경우
- `DecisionError`: 의사결정 과정에서 오류 발생 시

#### 예제

```python
# 기본 사용
result = kernel.decide(["rest", "work", "exercise"])
print(f"Decision: {result['action']}")
print(f"Probability: {result['probability']:.2f}")

# 외부 토크 주입
torque = {"choose_red": 0.3, "choose_blue": -0.1}
result = kernel.decide(["choose_red", "choose_blue"], external_torque=torque)
```

---

### `set_mode()`

인지 모드 변경

#### 시그니처

```python
def set_mode(self, mode: CognitiveMode | str) -> None
```

#### 파라미터

| 파라미터 | 타입 | 제약 | 기본값 | 설명 |
|---------|------|------|-------|------|
| `mode` | `CognitiveMode \| str` | enum 또는 문자열 | - | 인지 모드 |

#### 모드 목록

- `NORMAL`: 정상 모드
- `ADHD`: ADHD 모드 (고엔트로피, 강한 회전)
- `ASD`: ASD 모드 (저엔트로피, 약한 회전)
- `PTSD`: PTSD 모드
- `PANIC`: 공황 장애 모드
- `EPILEPSY`: 간질 모드
- `OCD`: 강박 장애 모드
- `IED`: 분노 조절 장애 모드
- `DEPRESSION`: 우울증 모드
- `BIPOLAR`: 양극성 장애 모드
- `DEMENTIA`: 치매 모드
- `ALZHEIMER`: 알츠하이머 모드

#### 문자열 모드 지원

- 문자열인 경우 대소문자 무시
- 예: `"adhd"`, `"ASD"`, `"Dementia"` 모두 유효

#### 예외

- `ModeError`: 유효하지 않은 모드인 경우

#### 예제

```python
# enum 사용
kernel.set_mode(CognitiveMode.ADHD)

# 문자열 사용 (대소문자 무시)
kernel.set_mode("adhd")
kernel.set_mode("ASD")
kernel.set_mode("dementia")
```

---

## 출력 스키마

### `decide()` 반환값 상세

```python
{
    "action": "work",  # 선택된 행동 (str, None 가능)
    "utility": 0.55,  # 선택된 행동의 utility (float)
    "probability": 0.44,  # 선택된 행동의 확률 (float)
    "probability_distribution": {  # 모든 옵션의 확률 분포
        "rest": 0.44,
        "work": 0.28,
        "exercise": 0.28
    },
    "entropy": 1.10,  # 선택 불확실성 (float)
    "core_strength": 0.5,  # 코어 강도 (float, 0.0 ~ 1.0)
    "habit_suggestion": None,  # 습관 제안 (Optional[str])
    "conflict": False,  # 갈등 여부 (bool)
    "cognitive_distress": False,  # 인지적 고통 여부 (bool)
    "distress_message": ""  # 고통 메시지 (str)
}
```

### `recall()` 반환값 상세

```python
[
    {
        "id": "c8337822-5ac0-434f-8a98-dc93ac0d591c",  # 기억 ID (str, UUID)
        "event_type": "meeting",  # 이벤트 종류 (str)
        "content": {"topic": "project"},  # 이벤트 내용 (Dict[str, Any])
        "importance": 0.9,  # 중요도 (float, 0.0 ~ 1.0)
        "timestamp": 1769950840.52  # Unix timestamp (float)
    },
    # ... 더 많은 기억들
]
```

---

## 에러 처리

### 검증 규칙

1. **importance, emotion**: 0.0 ~ 1.0 범위 (포함)
2. **k**: 양의 정수 (1 이상)
3. **options**: 비어있지 않은 문자열 리스트
4. **event_type**: 비어있지 않은 문자열
5. **timestamp**: 유효한 Unix timestamp (1970-01-01 ~ 2100-01-01)

### 예외 처리 정책

- **검증 실패**: `ValidationError` 발생
- **모드 오류**: `ModeError` 발생
- **의사결정 오류**: `DecisionError` 발생
- **메모리 오류**: `MemoryError` 발생

### 확률 분포 정규화

- `decide()`의 `probability_distribution`은 항상 정규화되어 합이 1.0입니다.
- 정규화는 내부적으로 자동 수행되며, 사용자는 별도 처리가 필요 없습니다.

---

## 예외 타입

### `CognitiveKernelError`

모든 Cognitive Kernel 예외의 기본 클래스

```python
class CognitiveKernelError(Exception):
    pass
```

### `ValidationError`

입력 검증 실패

```python
class ValidationError(CognitiveKernelError):
    pass
```

**발생 조건**:
- `importance`가 0.0 ~ 1.0 범위를 벗어남
- `k`가 양의 정수가 아님
- `options`가 빈 리스트
- `event_type`이 빈 문자열

### `ModeError`

인지 모드 관련 오류

```python
class ModeError(CognitiveKernelError):
    pass
```

**발생 조건**:
- 유효하지 않은 모드 문자열
- 모드 타입이 enum 또는 문자열이 아님

### `DecisionError`

의사결정 관련 오류

```python
class DecisionError(CognitiveKernelError):
    pass
```

### `MemoryError`

메모리 관련 오류

```python
class MemoryError(CognitiveKernelError):
    pass
```

---

## 버전 호환성

### v2.0.2 변경사항

1. **입력 검증 강화**: 모든 입력 파라미터에 대한 엄격한 검증 추가
2. **문자열 모드 지원**: `set_mode()`에서 문자열 모드 지원 (대소문자 무시)
3. **예외 타입 명확화**: 명확한 예외 타입 정의
4. **출력 스키마 고정**: `decide()`, `recall()` 반환값 구조 명시

### 하위 호환성

- v2.0.1과의 하위 호환성 유지
- 기존 코드는 수정 없이 동작

---

**작성자**: GNJz (Qquarts)  
**최종 업데이트**: 2026-02-01

