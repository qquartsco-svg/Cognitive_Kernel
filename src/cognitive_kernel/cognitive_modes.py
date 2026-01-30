"""
🧠 Cognitive Modes - 인지 성향 모드

ADHD와 ASD를 "탐색(Exploration) vs 착취(Exploitation)"의 극단으로 모델링:

- ADHD: 고엔트로피 (High Entropy) - 계속 시도하고 싶은 욕망 (+)
- ASD: 저엔트로피 (Low Entropy) - 패턴을 유지하고 싶은 욕망 (-)

수식:
    Entropy_Control = Exploration(ADHD) / Exploitation(ASD)

Author: GNJz (Qquarts)
Version: 2.0.0
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from enum import Enum


class CognitiveMode(Enum):
    """인지 모드"""
    NORMAL = "normal"
    ADHD = "adhd"  # 고엔트로피: 과도한 탐색
    ASD = "asd"    # 저엔트로피: 과도한 착취
    PTSD = "ptsd"  # 트라우마 고착


@dataclass
class ModeConfig:
    """모드별 파라미터 설정"""
    
    # Thalamus (입력 필터링)
    gate_threshold: float = 0.3  # 게이트 임계값 (낮을수록 모든 입력 허용)
    max_channels: int = 3  # 최대 통과 채널 수
    
    # PFC (의사결정)
    decision_temperature: float = 1.0  # Softmax 온도 (낮을수록 루틴 고착)
    working_memory_capacity: int = 7
    
    # BasalGanglia (탐색 vs 착취)
    tau: float = 0.5  # 탐색 온도 (낮을수록 착취 강화)
    impulsivity: Optional[float] = None  # 충동성
    patience: Optional[float] = None  # 인내심
    
    # MemoryRank (패턴 연결)
    damping: float = 0.85
    local_weight_boost: float = 1.0  # 로컬 연결 가중치 부스트
    
    # Amygdala (감정/위협)
    novelty_sensitivity: float = 1.0  # 신규성 민감도
    
    # Hypothalamus (에너지/스트레스)
    stress_baseline: float = 0.3
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            "thalamus": {
                "gate_threshold": self.gate_threshold,
                "max_channels": self.max_channels,
            },
            "pfc": {
                "decision_temperature": self.decision_temperature,
                "working_memory_capacity": self.working_memory_capacity,
            },
            "basal_ganglia": {
                "tau": self.tau,
                "impulsivity": self.impulsivity,
                "patience": self.patience,
            },
            "memoryrank": {
                "damping": self.damping,
                "local_weight_boost": self.local_weight_boost,
            },
            "amygdala": {
                "novelty_sensitivity": self.novelty_sensitivity,
            },
            "hypothalamus": {
                "stress_baseline": self.stress_baseline,
            },
        }


class CognitiveModePresets:
    """인지 모드 프리셋"""
    
    @staticmethod
    def normal() -> ModeConfig:
        """정상 모드 (균형)"""
        return ModeConfig(
            gate_threshold=0.3,
            max_channels=3,
            decision_temperature=1.0,
            working_memory_capacity=7,
            tau=0.5,
            impulsivity=None,
            patience=None,
            damping=0.85,
            local_weight_boost=1.0,
            novelty_sensitivity=1.0,
            stress_baseline=0.3,
        )
    
    @staticmethod
    def adhd() -> ModeConfig:
        """
        ADHD 모드: 고엔트로피 (High Entropy)
        
        특징:
        - 계속 시도하고 싶은 욕망 (+)
        - 과도한 탐색 (Over-Exploration)
        - 게이팅 임계값 높음 (산만함)
        - 온도 높음 (무작위적 의사결정)
        """
        return ModeConfig(
            gate_threshold=0.1,  # 낮은 임계값 → 모든 입력 통과 (산만)
            max_channels=10,  # 많은 채널 동시 처리
            decision_temperature=2.0,  # 높은 온도 → 탐색 강화
            working_memory_capacity=5,  # 낮은 용량 (집중력 부족)
            tau=1.5,  # 높은 탐색 온도
            impulsivity=0.8,  # 높은 충동성
            patience=0.2,  # 낮은 인내심
            damping=0.85,
            local_weight_boost=0.8,  # 글로벌 연결 선호
            novelty_sensitivity=2.0,  # 높은 신규성 민감도
            stress_baseline=0.4,
        )
    
    @staticmethod
    def asd() -> ModeConfig:
        """
        ASD 모드: 저엔트로피 (Low Entropy)
        
        특징:
        - 패턴을 유지하고 싶은 욕망 (-)
        - 과도한 착취 (Over-Exploitation)
        - 게이팅 임계값 낮음 (감각 과부하)
        - 온도 낮음 (루틴 고착)
        - 로컬 연결 강화 (패턴 고착)
        """
        return ModeConfig(
            gate_threshold=0.0,  # 모든 미세 자극 통과 (감각 과부하)
            max_channels=1,  # 단일 채널 집중
            decision_temperature=0.1,  # 매우 낮은 온도 → 루틴 고착
            working_memory_capacity=7,
            tau=0.1,  # 매우 낮은 탐색 온도 → 착취 강화
            impulsivity=0.1,  # 낮은 충동성
            patience=0.9,  # 높은 인내심 (루틴 유지)
            damping=0.85,
            local_weight_boost=3.0,  # 로컬 연결 강화 (패턴 고착)
            novelty_sensitivity=3.0,  # 높은 신규성 민감도 (낯선 상황 공포)
            stress_baseline=0.5,  # 높은 스트레스 기준선
        )
    
    @staticmethod
    def ptsd() -> ModeConfig:
        """
        PTSD 모드: 트라우마 고착
        
        특징:
        - 특정 기억에 비정상적으로 높은 가중치
        - 과각성 (Hyperarousal)
        - 예측 실패에 대한 높은 공포
        """
        return ModeConfig(
            gate_threshold=0.2,  # 낮은 임계값 (과각성)
            max_channels=5,
            decision_temperature=0.8,
            working_memory_capacity=5,
            tau=0.3,
            impulsivity=0.6,
            patience=0.3,
            damping=0.9,  # 높은 감쇠 (트라우마 기억 지속)
            local_weight_boost=2.0,  # 트라우마 노드 연결 강화
            novelty_sensitivity=2.5,  # 매우 높은 신규성 민감도
            stress_baseline=0.7,  # 높은 스트레스 기준선
        )
    
    @staticmethod
    def get_config(mode: CognitiveMode) -> ModeConfig:
        """모드에 따른 설정 반환"""
        if mode == CognitiveMode.NORMAL:
            return CognitiveModePresets.normal()
        elif mode == CognitiveMode.ADHD:
            return CognitiveModePresets.adhd()
        elif mode == CognitiveMode.ASD:
            return CognitiveModePresets.asd()
        elif mode == CognitiveMode.PTSD:
            return CognitiveModePresets.ptsd()
        else:
            raise ValueError(f"Unknown mode: {mode}")

