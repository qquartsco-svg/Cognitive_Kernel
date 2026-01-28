#!/usr/bin/env python3
"""
Cognitive Kernel - Full Brain Simulation (7 Engines)

7개 엔진 통합 파이프라인:
1. Thalamus    → 감각 입력 필터링
2. Amygdala    → 감정 처리, 위협 감지
3. Hypothalamus → 에너지/스트레스 조절
4. Panorama    → 이벤트 기록
5. MemoryRank  → 중요도 계산
6. PFC         → 의사결정
7. BasalGanglia → 행동 실행

시나리오: 하루 동안의 인지 시뮬레이션
- 정상 상태에서 시작
- 다양한 이벤트 발생 (일상, 스트레스, 위협)
- 시스템 반응 관찰
- 상태 변화 추적 및 분석
"""

import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import json

# 경로 설정
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "Thalamus"))
sys.path.insert(0, str(root / "Amygdala"))
sys.path.insert(0, str(root / "Hypothalamus"))
sys.path.insert(0, str(root / "Panorama" / "package"))
sys.path.insert(0, str(root / "MemoryRank" / "package"))
sys.path.insert(0, str(root / "PFC" / "package"))
sys.path.insert(0, str(root / "BasalGanglia" / "package"))

# 엔진 임포트
try:
    from thalamus import ThalamusEngine, ThalamusConfig, SensoryInput, ModalityType
except ImportError as e:
    print(f"⚠️ Thalamus import error: {e}")
    ThalamusEngine = None

try:
    from amygdala import AmygdalaEngine, AmygdalaConfig, ThreatSignal
except ImportError as e:
    print(f"⚠️ Amygdala import error: {e}")
    AmygdalaEngine = None

try:
    from hypothalamus import HypothalamusEngine, HypothalamusConfig, DriveType
except ImportError as e:
    print(f"⚠️ Hypothalamus import error: {e}")
    HypothalamusEngine = None

try:
    from panorama import PanoramaMemoryEngine, PanoramaConfig
except ImportError as e:
    print(f"⚠️ Panorama import error: {e}")
    PanoramaMemoryEngine = None

try:
    from memoryrank import MemoryRankEngine, MemoryRankConfig, MemoryNodeAttributes
except ImportError as e:
    print(f"⚠️ MemoryRank import error: {e}")
    MemoryRankEngine = None

try:
    from pfc import PFCEngine, PFCConfig, Action
except ImportError as e:
    print(f"⚠️ PFC import error: {e}")
    PFCEngine = None

try:
    from basal_ganglia import BasalGangliaEngine, BasalGangliaConfig
except ImportError as e:
    print(f"⚠️ BasalGanglia import error: {e}")
    BasalGangliaEngine = None


# ============================================================================
# 상태 추적 구조체
# ============================================================================

@dataclass
class BrainState:
    """전체 뇌 상태 스냅샷"""
    timestamp: float
    
    # Thalamus
    sensory_load: float = 0.0
    filtered_ratio: float = 0.0
    
    # Amygdala
    threat_level: float = 0.0
    arousal: float = 0.5
    valence: float = 0.0  # -1 (negative) ~ +1 (positive)
    
    # Hypothalamus
    energy: float = 1.0
    stress: float = 0.0
    homeostasis_deviation: float = 0.0
    
    # Panorama
    event_count: int = 0
    
    # MemoryRank
    top_memory_score: float = 0.0
    
    # PFC
    working_memory_load: int = 0
    decision_confidence: float = 0.0
    inhibition_active: bool = False
    
    # BasalGanglia
    habit_strength: float = 0.0
    action_type: str = "NONE"
    
    # 종합 지표
    cognitive_efficiency: float = 1.0
    
    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp,
            'thalamus': {'sensory_load': self.sensory_load, 'filtered_ratio': self.filtered_ratio},
            'amygdala': {'threat_level': self.threat_level, 'arousal': self.arousal, 'valence': self.valence},
            'hypothalamus': {'energy': self.energy, 'stress': self.stress},
            'panorama': {'event_count': self.event_count},
            'memoryrank': {'top_memory_score': self.top_memory_score},
            'pfc': {'working_memory_load': self.working_memory_load, 'confidence': self.decision_confidence},
            'basal_ganglia': {'habit_strength': self.habit_strength, 'action_type': self.action_type},
            'efficiency': self.cognitive_efficiency
        }


@dataclass
class SimulationEvent:
    """시뮬레이션 이벤트"""
    time: float
    event_type: str  # "normal", "stress", "threat", "reward", "fatigue"
    content: str
    intensity: float = 0.5
    modality: str = "EXTERNAL"


# ============================================================================
# Cognitive Kernel 통합 클래스
# ============================================================================

class CognitiveKernel:
    """
    7개 엔진 통합 인지 커널
    """
    
    def __init__(self):
        print("=" * 70)
        print("🧠 COGNITIVE KERNEL - Full Brain Simulation")
        print("=" * 70)
        
        # 엔진 초기화
        self._init_engines()
        
        # 상태 기록
        self.state_history: List[BrainState] = []
        self.event_log: List[Dict] = []
        self.current_time = 0.0
        
        # 분석 결과
        self.alerts: List[str] = []
        
    def _init_engines(self):
        """각 엔진 초기화"""
        
        # 1. Thalamus
        if ThalamusEngine:
            self.thalamus = ThalamusEngine(ThalamusConfig(
                gate_threshold=0.3,
                max_channels=10
            ))
            print("  ✅ Thalamus Engine initialized")
        else:
            self.thalamus = None
            print("  ⚠️ Thalamus Engine not available")
        
        # 2. Amygdala
        if AmygdalaEngine:
            self.amygdala = AmygdalaEngine(AmygdalaConfig(
                threat_threshold=0.5,
                extinction_rate=0.05
            ))
            print("  ✅ Amygdala Engine initialized")
        else:
            self.amygdala = None
            print("  ⚠️ Amygdala Engine not available")
        
        # 3. Hypothalamus
        if HypothalamusEngine:
            self.hypothalamus = HypothalamusEngine(HypothalamusConfig(
                energy_decay=0.01,
                stress_decrease=0.02
            ))
            print("  ✅ Hypothalamus Engine initialized")
        else:
            self.hypothalamus = None
            print("  ⚠️ Hypothalamus Engine not available")
        
        # 4. Panorama
        if PanoramaMemoryEngine:
            self.panorama = PanoramaMemoryEngine(PanoramaConfig(
                time_gap_threshold=300,  # 5분
                max_events=1000
            ))
            print("  ✅ Panorama Engine initialized")
        else:
            self.panorama = None
            print("  ⚠️ Panorama Engine not available")
        
        # 5. MemoryRank
        if MemoryRankEngine:
            self.memoryrank = MemoryRankEngine(MemoryRankConfig(
                damping=0.85,
                recency_weight=1.0,
                emotion_weight=1.5
            ))
            print("  ✅ MemoryRank Engine initialized")
        else:
            self.memoryrank = None
            print("  ⚠️ MemoryRank Engine not available")
        
        # 6. PFC
        if PFCEngine:
            self.pfc = PFCEngine(PFCConfig(
                working_memory_capacity=7,
                risk_aversion=0.5,
                inhibition_threshold=0.6
            ))
            print("  ✅ PFC Engine initialized")
        else:
            self.pfc = None
            print("  ⚠️ PFC Engine not available")
        
        # 7. BasalGanglia
        if BasalGangliaEngine:
            self.basal_ganglia = BasalGangliaEngine(BasalGangliaConfig(
                alpha=0.1,
                gamma=0.9,
                tau=0.5
            ))
            print("  ✅ BasalGanglia Engine initialized")
        else:
            self.basal_ganglia = None
            print("  ⚠️ BasalGanglia Engine not available")
        
        print("-" * 70)
    
    def process_event(self, event: SimulationEvent) -> BrainState:
        """
        이벤트 처리 파이프라인
        
        Flow:
        External → Thalamus → Amygdala → Hypothalamus
                              ↓
                          Panorama → MemoryRank → PFC → BasalGanglia
        """
        self.current_time = event.time
        state = BrainState(timestamp=event.time)
        
        # ─────────────────────────────────────────────────
        # [1] THALAMUS - 감각 입력 필터링
        # ─────────────────────────────────────────────────
        if self.thalamus and hasattr(self.thalamus, 'filter'):
            try:
                modality = ModalityType.EXTERNAL if event.modality == "EXTERNAL" else ModalityType.INTERNAL
                sensory_input = SensoryInput(
                    content=event.content,
                    modality=modality,
                    intensity=event.intensity
                )
                filtered = self.thalamus.filter([sensory_input])
                state.sensory_load = event.intensity
                state.filtered_ratio = len(filtered) / 1.0 if filtered else 0.0
            except Exception as e:
                state.sensory_load = event.intensity
                state.filtered_ratio = 1.0
        else:
            state.sensory_load = event.intensity
            state.filtered_ratio = 1.0
        
        # ─────────────────────────────────────────────────
        # [2] AMYGDALA - 감정 처리 및 위협 감지
        # ─────────────────────────────────────────────────
        if self.amygdala and hasattr(self.amygdala, 'process_threat'):
            try:
                if event.event_type == "threat":
                    threat = ThreatSignal(
                        source=event.content,
                        intensity=event.intensity,
                        context="simulation"
                    )
                    response = self.amygdala.process_threat(threat)
                    state.threat_level = response.threat_level if hasattr(response, 'threat_level') else event.intensity
                    state.arousal = min(1.0, 0.5 + event.intensity * 0.5)
                    state.valence = -0.5 * event.intensity
                elif event.event_type == "reward":
                    state.threat_level = 0.0
                    state.arousal = 0.6
                    state.valence = 0.5 * event.intensity
                else:
                    state.threat_level = 0.1 if event.event_type == "stress" else 0.0
                    state.arousal = 0.5 + event.intensity * 0.2
                    state.valence = 0.0
            except Exception as e:
                state.arousal = 0.5 + event.intensity * 0.3
                state.valence = -0.3 if event.event_type in ["threat", "stress"] else 0.1
        else:
            # 간단한 감정 계산
            if event.event_type == "threat":
                state.threat_level = event.intensity
                state.arousal = min(1.0, 0.5 + event.intensity * 0.5)
                state.valence = -0.5 * event.intensity
            elif event.event_type == "stress":
                state.threat_level = event.intensity * 0.3
                state.arousal = 0.5 + event.intensity * 0.3
                state.valence = -0.2 * event.intensity
            elif event.event_type == "reward":
                state.threat_level = 0.0
                state.arousal = 0.6
                state.valence = 0.5 * event.intensity
            else:
                state.threat_level = 0.0
                state.arousal = 0.5
                state.valence = 0.0
        
        # ─────────────────────────────────────────────────
        # [3] HYPOTHALAMUS - 에너지 및 스트레스 조절
        # ─────────────────────────────────────────────────
        if self.hypothalamus and hasattr(self.hypothalamus, 'update'):
            try:
                # 에너지 소모 계산
                energy_cost = 0.02 * event.intensity
                if event.event_type in ["threat", "stress"]:
                    energy_cost *= 2.0
                
                # 스트레스 추가
                stress_input = 0.0
                if event.event_type == "threat":
                    stress_input = event.intensity * 0.5
                elif event.event_type == "stress":
                    stress_input = event.intensity * 0.3
                
                self.hypothalamus.update(
                    energy_consumption=energy_cost,
                    stress_input=stress_input,
                    dt=1.0
                )
                internal = self.hypothalamus.get_state()
                state.energy = internal.energy if hasattr(internal, 'energy') else 0.8
                state.stress = internal.stress if hasattr(internal, 'stress') else stress_input
            except Exception as e:
                # 수동 계산
                if len(self.state_history) > 0:
                    prev = self.state_history[-1]
                    state.energy = max(0.0, prev.energy - 0.02 * event.intensity)
                    if event.event_type in ["threat", "stress"]:
                        state.stress = min(1.0, prev.stress + event.intensity * 0.2)
                    else:
                        state.stress = max(0.0, prev.stress - 0.05)
                else:
                    state.energy = 1.0 - 0.02 * event.intensity
                    state.stress = event.intensity * 0.2 if event.event_type in ["threat", "stress"] else 0.0
        else:
            # 간단한 에너지/스트레스 계산
            if len(self.state_history) > 0:
                prev = self.state_history[-1]
                state.energy = max(0.0, prev.energy - 0.02 * event.intensity)
                if event.event_type in ["threat", "stress"]:
                    state.stress = min(1.0, prev.stress + event.intensity * 0.2)
                else:
                    state.stress = max(0.0, prev.stress - 0.05)
            else:
                state.energy = 1.0 - 0.02 * event.intensity
                state.stress = event.intensity * 0.2 if event.event_type in ["threat", "stress"] else 0.0
        
        # ─────────────────────────────────────────────────
        # [4] PANORAMA - 이벤트 기록
        # ─────────────────────────────────────────────────
        if self.panorama:
            try:
                self.panorama.append_event(
                    timestamp=event.time,
                    event_type=event.event_type,
                    payload={
                        'content': event.content,
                        'intensity': event.intensity,
                        'arousal': state.arousal,
                        'valence': state.valence
                    },
                    importance=abs(state.valence) * state.arousal
                )
                state.event_count = len(self.panorama._events) if hasattr(self.panorama, '_events') else 0
            except Exception as e:
                pass
        
        # ─────────────────────────────────────────────────
        # [5] MEMORYRANK - 중요도 계산 (이벤트 간 연결)
        # ─────────────────────────────────────────────────
        if self.memoryrank and len(self.state_history) > 0:
            try:
                # 이전 이벤트와 연결 구축
                edges = []
                prev_event_id = f"event_{len(self.state_history) - 1}"
                curr_event_id = f"event_{len(self.state_history)}"
                
                # 순차적 연결
                edges.append((prev_event_id, curr_event_id, 1.0))
                
                # 유사 이벤트 연결 (같은 타입)
                for i, prev_state in enumerate(self.state_history[-5:]):
                    if i < len(self.event_log) and self.event_log[-(5-i)]['type'] == event.event_type:
                        edges.append((f"event_{len(self.state_history) - 5 + i}", curr_event_id, 0.5))
                
                # 노드 속성
                node_attrs = {
                    curr_event_id: MemoryNodeAttributes(
                        recency=1.0,
                        emotion=abs(state.valence),
                        frequency=1.0
                    )
                }
                
                if edges:
                    self.memoryrank.build_graph(edges, node_attrs)
                    scores = self.memoryrank.calculate_importance()
                    state.top_memory_score = max(scores.values()) if scores else 0.0
            except Exception as e:
                pass
        
        # ─────────────────────────────────────────────────
        # [6] PFC - 의사결정
        # ─────────────────────────────────────────────────
        if self.pfc:
            try:
                # 후보 행동 정의
                actions = [
                    Action(id="1", name="continue", expected_reward=0.3, effort_cost=0.1, risk=0.1),
                    Action(id="2", name="rest", expected_reward=0.5, effort_cost=0.05, risk=0.05),
                    Action(id="3", name="avoid", expected_reward=0.2, effort_cost=0.2, risk=0.3),
                    Action(id="4", name="engage", expected_reward=0.7, effort_cost=0.4, risk=0.2),
                ]
                
                # 위협 시 회피 보상 증가
                if state.threat_level > 0.5:
                    actions[2] = Action(id="3", name="avoid", expected_reward=0.8, effort_cost=0.1, risk=0.1)
                
                # 에너지 부족 시 휴식 보상 증가
                if state.energy < 0.3:
                    actions[1] = Action(id="2", name="rest", expected_reward=0.9, effort_cost=0.01, risk=0.01)
                
                selected = self.pfc.select_action(actions)
                if selected:
                    state.decision_confidence = self.pfc.evaluate_action(selected)
                    # 억제 확인
                    state.inhibition_active = state.stress > 0.6 or state.energy < 0.2
                
                state.working_memory_load = len(self.pfc._working_memory) if hasattr(self.pfc, '_working_memory') else 0
            except Exception as e:
                pass
        
        # ─────────────────────────────────────────────────
        # [7] BASALGANGLIA - 행동 실행
        # ─────────────────────────────────────────────────
        if self.basal_ganglia:
            try:
                context = f"{event.event_type}_{int(state.energy * 10)}"
                actions = ["continue", "rest", "avoid", "engage"]
                
                result = self.basal_ganglia.select_action(context, actions)
                if result and result.action:
                    state.action_type = result.action_type.value if hasattr(result.action_type, 'value') else str(result.action_type)
                    state.habit_strength = result.action.habit_strength if hasattr(result.action, 'habit_strength') else 0.0
                    
                    # 학습
                    reward = 0.5
                    if event.event_type == "reward":
                        reward = 0.8
                    elif event.event_type == "threat" and result.action.name == "avoid":
                        reward = 0.7
                    elif event.event_type == "fatigue" and result.action.name == "rest":
                        reward = 0.8
                    
                    self.basal_ganglia.learn(context, result.action.name, reward)
            except Exception as e:
                state.action_type = "fallback"
        
        # ─────────────────────────────────────────────────
        # 종합 인지 효율 계산
        # ─────────────────────────────────────────────────
        state.cognitive_efficiency = (
            state.energy * 0.3 +
            (1.0 - state.stress) * 0.2 +
            (1.0 - state.threat_level) * 0.2 +
            state.filtered_ratio * 0.1 +
            state.decision_confidence * 0.2
        )
        
        # 상태 기록
        self.state_history.append(state)
        self.event_log.append({
            'time': event.time,
            'type': event.event_type,
            'content': event.content,
            'intensity': event.intensity
        })
        
        # 이상 탐지
        self._check_alerts(state, event)
        
        return state
    
    def _check_alerts(self, state: BrainState, event: SimulationEvent):
        """이상 상태 탐지"""
        
        # 에너지 고갈
        if state.energy < 0.2:
            self.alerts.append(f"⚠️ [t={state.timestamp:.1f}] ENERGY CRITICAL: {state.energy:.2f}")
        
        # 과각성
        if state.arousal > 0.85:
            self.alerts.append(f"⚠️ [t={state.timestamp:.1f}] HYPERAROUSAL: {state.arousal:.2f}")
        
        # 만성 스트레스
        if state.stress > 0.7:
            self.alerts.append(f"⚠️ [t={state.timestamp:.1f}] HIGH STRESS: {state.stress:.2f}")
        
        # 억제 실패
        if state.inhibition_active and state.stress > 0.8:
            self.alerts.append(f"⚠️ [t={state.timestamp:.1f}] INHIBITION OVERLOAD")
        
        # 인지 효율 저하
        if state.cognitive_efficiency < 0.4:
            self.alerts.append(f"⚠️ [t={state.timestamp:.1f}] LOW EFFICIENCY: {state.cognitive_efficiency:.2f}")
    
    def run_simulation(self, events: List[SimulationEvent]) -> List[BrainState]:
        """시뮬레이션 실행"""
        print("\n" + "=" * 70)
        print("🚀 SIMULATION START")
        print("=" * 70)
        
        for event in events:
            state = self.process_event(event)
            self._print_step(event, state)
        
        return self.state_history
    
    def _print_step(self, event: SimulationEvent, state: BrainState):
        """단계 출력"""
        print(f"\n[T={event.time:5.1f}] {event.event_type.upper():8s} | {event.content[:30]:30s}")
        print(f"         Energy: {state.energy:.2f} | Stress: {state.stress:.2f} | Arousal: {state.arousal:.2f} | Efficiency: {state.cognitive_efficiency:.2f}")
    
    def analyze(self) -> Dict:
        """시뮬레이션 분석"""
        if not self.state_history:
            return {"error": "No simulation data"}
        
        print("\n" + "=" * 70)
        print("📊 ANALYSIS REPORT")
        print("=" * 70)
        
        # 통계
        energies = [s.energy for s in self.state_history]
        stresses = [s.stress for s in self.state_history]
        arousals = [s.arousal for s in self.state_history]
        efficiencies = [s.cognitive_efficiency for s in self.state_history]
        
        analysis = {
            "total_events": len(self.state_history),
            "energy": {
                "start": energies[0],
                "end": energies[-1],
                "min": min(energies),
                "mean": sum(energies) / len(energies)
            },
            "stress": {
                "max": max(stresses),
                "mean": sum(stresses) / len(stresses),
                "chronic_periods": sum(1 for s in stresses if s > 0.6)
            },
            "arousal": {
                "max": max(arousals),
                "mean": sum(arousals) / len(arousals),
                "hyperarousal_count": sum(1 for a in arousals if a > 0.8)
            },
            "efficiency": {
                "mean": sum(efficiencies) / len(efficiencies),
                "min": min(efficiencies),
                "low_periods": sum(1 for e in efficiencies if e < 0.5)
            },
            "alerts": self.alerts
        }
        
        # 출력
        print(f"\n📈 Energy Trajectory:")
        print(f"   Start: {analysis['energy']['start']:.2f} → End: {analysis['energy']['end']:.2f}")
        print(f"   Min: {analysis['energy']['min']:.2f} | Mean: {analysis['energy']['mean']:.2f}")
        
        print(f"\n😰 Stress Analysis:")
        print(f"   Max: {analysis['stress']['max']:.2f} | Mean: {analysis['stress']['mean']:.2f}")
        print(f"   Chronic periods (>0.6): {analysis['stress']['chronic_periods']}")
        
        print(f"\n⚡ Arousal Analysis:")
        print(f"   Max: {analysis['arousal']['max']:.2f} | Mean: {analysis['arousal']['mean']:.2f}")
        print(f"   Hyperarousal events (>0.8): {analysis['arousal']['hyperarousal_count']}")
        
        print(f"\n🎯 Cognitive Efficiency:")
        print(f"   Mean: {analysis['efficiency']['mean']:.2f} | Min: {analysis['efficiency']['min']:.2f}")
        print(f"   Low efficiency periods (<0.5): {analysis['efficiency']['low_periods']}")
        
        if self.alerts:
            print(f"\n🚨 ALERTS ({len(self.alerts)}):")
            for alert in self.alerts[-10:]:  # 최근 10개
                print(f"   {alert}")
        
        # 진단
        print("\n" + "-" * 70)
        print("🔍 DIAGNOSTIC SUMMARY:")
        
        issues = []
        if analysis['energy']['end'] < 0.3:
            issues.append("• Energy Depletion: 에너지 고갈 위험 - 휴식 필요")
        if analysis['stress']['chronic_periods'] > len(self.state_history) * 0.3:
            issues.append("• Chronic Stress: 만성 스트레스 패턴 감지 - 스트레스 관리 필요")
        if analysis['arousal']['hyperarousal_count'] > 3:
            issues.append("• Hyperarousal Pattern: 과각성 반복 - 이완 기법 권장")
        if analysis['efficiency']['mean'] < 0.5:
            issues.append("• Low Cognitive Performance: 전반적 인지 효율 저하")
        
        if issues:
            for issue in issues:
                print(f"   {issue}")
        else:
            print("   ✅ 정상 범위 내 작동")
        
        return analysis


# ============================================================================
# 시나리오 생성
# ============================================================================

def create_day_scenario() -> List[SimulationEvent]:
    """하루 시나리오 생성"""
    events = []
    t = 0.0
    
    # 아침 (0-2시간)
    events.append(SimulationEvent(t, "normal", "Morning wake up", 0.3))
    t += 1.0
    events.append(SimulationEvent(t, "normal", "Breakfast", 0.2))
    t += 1.0
    
    # 출근/활동 시작 (2-4시간)
    events.append(SimulationEvent(t, "normal", "Commute to work", 0.4))
    t += 1.0
    events.append(SimulationEvent(t, "normal", "Start working", 0.5))
    t += 1.0
    
    # 스트레스 이벤트 (4-6시간)
    events.append(SimulationEvent(t, "stress", "Urgent deadline", 0.7))
    t += 1.0
    events.append(SimulationEvent(t, "stress", "Multiple requests", 0.6))
    t += 1.0
    
    # 위협 이벤트 (6-7시간)
    events.append(SimulationEvent(t, "threat", "Angry customer call", 0.8))
    t += 1.0
    
    # 휴식 (7-8시간)
    events.append(SimulationEvent(t, "reward", "Lunch break", 0.5))
    t += 1.0
    
    # 오후 업무 (8-10시간)
    events.append(SimulationEvent(t, "normal", "Afternoon tasks", 0.5))
    t += 1.0
    events.append(SimulationEvent(t, "stress", "Technical issue", 0.6))
    t += 1.0
    
    # 피로 (10-12시간)
    events.append(SimulationEvent(t, "fatigue", "Mental fatigue", 0.7, "INTERNAL"))
    t += 1.0
    events.append(SimulationEvent(t, "normal", "End of work", 0.3))
    t += 1.0
    
    # 저녁 회복 (12-14시간)
    events.append(SimulationEvent(t, "reward", "Dinner with friends", 0.6))
    t += 1.0
    events.append(SimulationEvent(t, "normal", "Relaxation", 0.2))
    t += 1.0
    
    return events


def create_ptsd_scenario() -> List[SimulationEvent]:
    """PTSD 시나리오 (반복 위협 + 과각성)"""
    events = []
    t = 0.0
    
    events.append(SimulationEvent(t, "normal", "Normal morning", 0.3))
    t += 1.0
    events.append(SimulationEvent(t, "threat", "Trauma trigger", 0.9))
    t += 1.0
    events.append(SimulationEvent(t, "threat", "Flashback", 0.85))
    t += 1.0
    events.append(SimulationEvent(t, "stress", "Avoidance behavior", 0.7))
    t += 1.0
    events.append(SimulationEvent(t, "threat", "Another trigger", 0.8))
    t += 1.0
    events.append(SimulationEvent(t, "stress", "Hypervigilance", 0.75))
    t += 1.0
    events.append(SimulationEvent(t, "fatigue", "Emotional exhaustion", 0.8, "INTERNAL"))
    t += 1.0
    events.append(SimulationEvent(t, "normal", "Attempt to rest", 0.3))
    t += 1.0
    
    return events


# ============================================================================
# 메인
# ============================================================================

def main():
    # 커널 초기화
    kernel = CognitiveKernel()
    
    print("\n" + "=" * 70)
    print("📋 SCENARIO SELECTION")
    print("=" * 70)
    print("  1. Normal Day Scenario (정상 하루)")
    print("  2. PTSD Scenario (PTSD 패턴)")
    print("-" * 70)
    
    # 정상 하루 시나리오 실행
    print("\n▶ Running Normal Day Scenario...")
    events = create_day_scenario()
    kernel.run_simulation(events)
    analysis1 = kernel.analyze()
    
    print("\n\n" + "=" * 70)
    print("▶ Running PTSD Scenario...")
    print("=" * 70)
    
    # PTSD 시나리오
    kernel2 = CognitiveKernel()
    events2 = create_ptsd_scenario()
    kernel2.run_simulation(events2)
    analysis2 = kernel2.analyze()
    
    # 비교
    print("\n\n" + "=" * 70)
    print("📊 COMPARISON: Normal vs PTSD")
    print("=" * 70)
    print(f"{'Metric':<30} {'Normal':>15} {'PTSD':>15}")
    print("-" * 60)
    print(f"{'Energy (end)':<30} {analysis1['energy']['end']:>15.2f} {analysis2['energy']['end']:>15.2f}")
    print(f"{'Stress (max)':<30} {analysis1['stress']['max']:>15.2f} {analysis2['stress']['max']:>15.2f}")
    print(f"{'Hyperarousal events':<30} {analysis1['arousal']['hyperarousal_count']:>15} {analysis2['arousal']['hyperarousal_count']:>15}")
    print(f"{'Efficiency (mean)':<30} {analysis1['efficiency']['mean']:>15.2f} {analysis2['efficiency']['mean']:>15.2f}")
    print(f"{'Total alerts':<30} {len(analysis1['alerts']):>15} {len(analysis2['alerts']):>15}")
    
    print("\n✅ Simulation Complete!")


if __name__ == "__main__":
    main()

