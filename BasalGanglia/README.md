# Basal Ganglia Engine (기저핵 엔진)

**Version**: 1.0.0-alpha  
**Status**: 소프트웨어 벤치마킹 단계 (물리적 하드웨어 테스트 미완)  
**License**: MIT License  
**Author**: GNJz (Qquarts)

---

## ⚠️ 중요 안내

**현재 상태**: 본 엔진은 소프트웨어 시뮬레이션 및 벤치마킹 단계에 있습니다.  
**물리적 하드웨어 테스트는 아직 완료되지 않았으며**, 실제 산업 환경에 적용하기 전에 추가 검증이 필요합니다.

본 프로젝트는 **계속 발전하는 구조**이며, 테스트 과정과 계획된 업그레이드를 통해 확장되어 갑니다.

---

## 📋 개요

**Basal Ganglia Engine**은 산업용 행동 선택 및 습관 형성 시스템을 목표로 하는 소프트웨어 엔진입니다. 생물학적 기저핵의 기능을 모사하여 행동 선택(Go/NoGo), 습관 형성, 보상 기반 학습 등의 기능을 제공합니다.

### 핵심 기능

- ✅ **행동 선택**: 여러 행동 옵션 중 최적 행동 선택 (Go/NoGo/Explore)
- ✅ **습관 형성**: 반복된 행동의 자동화 (Fast Path)
- ✅ **보상 학습**: Q-learning 기반 강화학습 (TD-Learning)
- ✅ **도파민 통합**: 도파민 신호 기반 학습률 조절
- ✅ **탐색-활용 균형**: 소프트맥스 기반 확률적 선택

---

## 🎯 예상 산업 활용 분야

**참고**: 아래는 본 엔진의 잠재적 활용 분야이며, 실제 적용을 위해서는 추가 검증이 필요합니다.

### 1. 로봇 행동 선택 시스템 (예상)
- 여러 행동 옵션 중 최적 행동 선택
- 반복 작업의 자동화 (습관 형성)
- 보상 기반 학습을 통한 행동 개선

### 2. 게임 AI 행동 시스템 (예상)
- NPC의 행동 선택 및 습관 형성
- 보상 기반 학습을 통한 행동 패턴 개선
- 개성 있는 캐릭터 행동 패턴

### 3. 자율 시스템 제어 (예상)
- 다중 옵션 중 최적 선택
- 반복 작업의 자동화
- 보상 기반 최적화

---

## 🚀 빠른 시작

### 설치

```bash
pip install -r requirements.txt
```

### 기본 사용법

```python
from basal_ganglia import BasalGangliaEngine, BasalGangliaConfig

# 설정
config = BasalGangliaConfig(
    alpha=0.1,              # 학습률
    gamma=0.9,              # 할인율
    habit_threshold=0.7     # 습관화 임계값
)

# 엔진 초기화
engine = BasalGangliaEngine(config)

# 행동 선택
context = "인사 상황"
possible_actions = ["안녕하세요", "반갑습니다", "하이"]
result = engine.select_action(context, possible_actions)

print(f"선택된 행동: {result.action.name}")
print(f"결정: {result.decision.value}")
print(f"자동 실행: {result.is_automatic}")

# 학습
engine.learn(context, "안녕하세요", reward=0.8)

# 습관 확인
habits = engine.get_habits()
print(f"형성된 습관: {len(habits)}개")
```

---

## 📐 핵심 수식

### 1. Q-value 업데이트 (TD-Learning)

```
Q(s,a) ← Q(s,a) + α[R + γ·max(Q(s',a')) - Q(s,a)]
```

- **α (alpha)**: 학습률
- **γ (gamma)**: 할인율 (미래 보상 중시도)
- **R**: 현재 보상
- **max(Q(s',a'))**: 다음 상태의 최대 Q-값

### 2. 행동 선택 (Softmax)

```
P(a) = exp(Q(s,a) / τ) / Σ exp(Q(s',a') / τ)
```

- **τ (tau)**: 소프트맥스 온도 (탐색 vs 활용)
- **Q(s,a)**: 행동 a의 Q-값

### 3. 습관 강도 업데이트

```
H = H + β·(1 - H)  (성공 시)
H = H - (β/2)·H     (실패 시)
```

- **H**: 습관 강도 (0~1)
- **β (beta)**: 습관 강화율

### 4. 도파민 보정

```
learning_rate = α · (1.0 + dopamine_boost)
dopamine_boost = (dopamine_level - baseline) · boost_factor
```

- 도파민이 높으면 학습률 증가
- 도파민이 낮으면 학습률 감소

---

## 🧠 생물학적 모델

### 기저핵 구조

- **Striatum (선조체)**: 입력, 상황-행동 매핑
- **GPi/SNr (담창구)**: 출력, Go/NoGo 결정
- **STN (시상하핵)**: 억제 조절

### 학습 메커니즘

- **도파민 신호**: 보상 예측 오차 (TD error)
- **습관 형성**: 반복된 행동의 자동화
- **행동 선택**: 여러 옵션 중 하나만 실행 (나머지 억제)

---

## 📦 API 문서

### BasalGangliaEngine

#### `__init__(config=None, use_hash=False)`

엔진 초기화

**Parameters:**
- `config` (BasalGangliaConfig, optional): 설정 객체
- `use_hash` (bool): 긴 컨텍스트를 해시로 저장 (메모리 최적화)

#### `select_action(context, possible_actions, allow_exploration=True)`

행동 선택

**Parameters:**
- `context` (str): 현재 상황/맥락
- `possible_actions` (List[str]): 가능한 행동 목록
- `allow_exploration` (bool): 탐색 허용 여부

**Returns:**
- `ActionResult`: 선택된 행동과 결정 정보

#### `learn(context, action_name, reward, next_context=None)`

보상 학습 (TD-Learning)

**Parameters:**
- `context` (str): 상황
- `action_name` (str): 실행한 행동
- `reward` (float): 받은 보상 (-1 ~ +1)
- `next_context` (str, optional): 다음 상황

#### `set_dopamine_level(level)`

도파민 레벨 설정

**Parameters:**
- `level` (float): 도파민 레벨 (0.0 ~ 1.0)

#### `get_habits()`

모든 습관화된 행동 반환

**Returns:**
- `List[Action]`: 습관화된 행동 목록

#### `get_state()`

전체 상태 반환

**Returns:**
- `Dict`: 상태 정보 (도파민, 컨텍스트 수, 행동 수, 습관 등)

---

## 🧪 테스트

### 단위 테스트 실행

```bash
PYTHONPATH=./package python3 -m pytest tests/ -v
```

### 예제 실행

```bash
PYTHONPATH=./package python3 examples/basic_usage.py
```

---

## 📊 성능 지표

**참고**: 아래는 소프트웨어 벤치마킹 결과이며, 실제 산업 환경에서는 다를 수 있습니다.

- **행동 선택 시간**: < 1ms (평균)
- **학습 업데이트 시간**: < 0.5ms (평균)
- **습관 형성**: 약 30-50회 반복 학습 후 습관화 (설정에 따라 다름)

---

## 🔧 설정 옵션

### BasalGangliaConfig

- `alpha` (float): 학습률 (기본값: 0.1)
- `gamma` (float): 할인율 (기본값: 0.9)
- `tau` (float): 소프트맥스 온도 (기본값: 0.5)
- `habit_threshold` (float): 습관화 임계값 (기본값: 0.7)
- `habit_beta` (float): 습관 강화율 (기본값: 0.1)
- `decay_rate` (float): Q-값 감쇠율 (기본값: 0.01)
- `exploration_bonus` (float): 탐색 보너스 (기본값: 0.2)
- `dopamine_baseline` (float): 도파민 기준선 (기본값: 0.5)
- `impulsivity` (float, optional): 충동성 (0~1)
- `patience` (float, optional): 인내심 (0~1)

---

## 🔗 다른 엔진과의 통합

### Hypothalamus Engine 연동

```python
from hypothalamus import HypothalamusEngine
from basal_ganglia import BasalGangliaEngine

hypo = HypothalamusEngine()
bg = BasalGangliaEngine()

# 시상하부의 도파민 레벨을 기저핵에 주입
dopamine = hypo.get_state()['dopamine']
bg.set_dopamine_level(dopamine)
```

---

## 📚 참고 논문

- **Schultz (1997)**: Dopamine reward prediction error
- **Graybiel (2008)**: Habits, rituals, and the evaluative brain
- **Frank (2005)**: Go/NoGo model of basal ganglia

---

## 📝 변경 이력

### v1.0.0-alpha (2025-01-XX)
- 초기 릴리스
- 행동 선택 기능
- 습관 형성 기능
- 보상 학습 기능
- 도파민 통합

---

## 🤝 기여

본 프로젝트는 오픈소스이며, 자유롭게 연구, 재사용, 확장이 가능합니다.

---

## 📄 라이선스

MIT License

---

## 🔗 관련 링크

- [GitHub Repository](https://github.com/qquartsco-svg/Basal_Ganglia_engine)
- [블록체인 기반 기여도 시스템](./BLOCKCHAIN_INFO.md)

---

## 💬 문의

문의사항이 있으시면 GitHub Issues를 통해 연락해 주세요.

