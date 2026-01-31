"""
🧠 Cognitive Modes - 인지 성향 모드

ADHD와 ASD를 "탐색(Exploration) vs 착취(Exploitation)"의 극단으로 모델링:

- ADHD: 고엔트로피 (High Entropy) - 계속 시도하고 싶은 욕망 (+)
- ASD: 저엔트로피 (Low Entropy) - 패턴을 유지하고 싶은 욕망 (-)

개념적 수식 (비율 표현):
    Entropy_Control = Exploration(ADHD) / Exploitation(ASD)
    
    주의: 이는 개념적 비율 표현이며, 실제 계산되는 수치가 아닙니다.
    실제 구현은 각 모드의 파라미터 조합으로 동작합니다.

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
    
    # ADHD(+) ↔ ASD(-) 극 사이 질환들
    PANIC = "panic"           # 공황장애: 과각성, 높은 불안
    EPILEPSY = "epilepsy"     # 간질: 불안정, 발작
    OCD = "ocd"               # 강박: 고착, 반복 행동
    IED = "ied"               # 분노조절장애: 충동, 폭발적 분노
    DEPRESSION = "depression" # 우울증: 무기력, 부정적 편향
    BIPOLAR = "bipolar"       # 양극성 장애: 조증 ↔ 우울


@dataclass
class ModeConfig:
    """모드별 파라미터 설정"""
    
    # Thalamus (입력 필터링)
    gate_threshold: float = 0.3  # 게이트 임계값 θ (0~1, 낮을수록 모든 입력 허용, 높을수록 필터링 강화)
    max_channels: int = 3  # 최대 통과 채널 수 (주의 자원 제한)
    
    # PFC (의사결정)
    decision_temperature: float = 1.0  # Softmax inverse-temperature β (P(i) = exp(β×U_i) / Σexp(β×U_j))
                                       # β ↑ (temperature ↓) → 효용 차이 강조 (결정론적, 루틴 고착)
                                       # β ↓ (temperature ↑) → 무작위성 증가 (탐색 강화)
    working_memory_capacity: int = 7
    
    # BasalGanglia (탐색 vs 착취)
    tau: float = 0.5  # Softmax 온도 τ (P(a) = exp(Q(s,a)/τ) / Σexp(Q(s,a')/τ))
                     # 낮을수록 높은 Q값 강조 (착취 강화), 높을수록 균등 선택 (탐색 강화)
    impulsivity: Optional[float] = None  # 충동성 (0~1, 높을수록 탐색↑, 습관 형성↑)
    patience: Optional[float] = None  # 인내심 (0~1, 높을수록 미래 보상 중시, gamma↑)
    
    # MemoryRank (패턴 연결)
    damping: float = 0.85
    local_weight_boost: float = 1.0  # 로컬 연결 가중치 부스트 (개념적 파라미터, 향후 구현)
    
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
        - 게이팅 임계값 낮음 (산만함) - 낮은 임계값으로 모든 입력 통과
        - decision_temperature 낮음 (β↓) → 무작위성 증가 (탐색 강화)
        """
        return ModeConfig(
            gate_threshold=0.1,  # 낮은 임계값 → 모든 입력 통과 (산만)
            max_channels=10,  # 많은 채널 동시 처리
            decision_temperature=0.5,  # β↓ (temperature↑) → 무작위성 증가 (탐색 강화)
            working_memory_capacity=5,  # 낮은 용량 (집중력 부족)
            tau=1.5,  # 높은 tau → 탐색 강화 (Q값 차이 덜 중요)
            impulsivity=0.8,  # 높은 충동성
            patience=0.2,  # 낮은 인내심
            damping=0.85,
            local_weight_boost=0.8,  # 글로벌 연결 선호 (개념적, 향후 구현)
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
        - decision_temperature 높음 (β↑, temperature↓) → 효용 차이 강조 (결정론적, 루틴 고착)
        - 로컬 연결 강화 (패턴 고착)
        """
        return ModeConfig(
            gate_threshold=0.0,  # 모든 미세 자극 통과 (감각 과부하)
            max_channels=1,  # 단일 채널 집중
            decision_temperature=5.0,  # β↑ (temperature↓) → 효용 차이 강조 (결정론적, 루틴 고착)
            working_memory_capacity=7,
            tau=0.1,  # 매우 낮은 탐색 온도 → 착취 강화
            impulsivity=0.1,  # 낮은 충동성
            patience=0.9,  # 높은 인내심 (루틴 유지)
            damping=0.85,
            local_weight_boost=3.0,  # 로컬 연결 강화 (패턴 고착, 개념적, 향후 구현)
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
            local_weight_boost=2.0,  # 트라우마 노드 연결 강화 (개념적, 향후 구현)
            novelty_sensitivity=2.5,  # 매우 높은 신규성 민감도
            stress_baseline=0.7,  # 높은 스트레스 기준선
        )
    
    @staticmethod
    def panic() -> ModeConfig:
        """
        공황장애 모드: 과각성, 높은 불안
        
        특징:
        - 갑작스러운 공황 발작
        - 과각성 (Hyperarousal)
        - 높은 불안/스트레스
        - ADHD 쪽에 가깝지만 불안 차원이 높음
        """
        return ModeConfig(
            gate_threshold=0.15,  # 낮은 임계값 (과각성)
            max_channels=8,  # 많은 채널 (불안으로 인한 산만)
            decision_temperature=0.6,  # 중간 (불안정)
            working_memory_capacity=4,  # 낮은 용량 (공황 시 집중력 저하)
            tau=1.2,  # 높은 탐색
            impulsivity=0.7,  # 높은 충동성
            patience=0.2,  # 낮은 인내심
            damping=0.85,
            local_weight_boost=1.0,
            novelty_sensitivity=3.5,  # 매우 높은 신규성 민감도 (공포)
            stress_baseline=0.8,  # 매우 높은 스트레스
        )
    
    @staticmethod
    def epilepsy() -> ModeConfig:
        """
        간질 모드: 불안정, 발작
        
        특징:
        - 뇌 전기 활동 이상
        - 발작 (Seizure)
        - 극도의 불안정성
        - ADHD 쪽 (불안정, 탐색)
        """
        return ModeConfig(
            gate_threshold=0.2,  # 낮은 임계값 (불안정)
            max_channels=6,  # 중간
            decision_temperature=0.4,  # 낮음 (매우 불안정)
            working_memory_capacity=5,  # 낮음
            tau=2.0,  # 매우 높은 탐색 (불안정)
            impulsivity=0.9,  # 매우 높은 충동성
            patience=0.1,  # 매우 낮은 인내심
            damping=0.85,
            local_weight_boost=0.8,  # 글로벌 연결 선호
            novelty_sensitivity=2.0,  # 높은 민감도
            stress_baseline=0.6,  # 높은 스트레스
        )
    
    @staticmethod
    def ocd() -> ModeConfig:
        """
        강박 모드: 고착, 반복 행동
        
        특징:
        - 반복 행동 (Compulsion)
        - 고착 (Obsession)
        - 불안 완화를 위한 의식
        - ASD 쪽에 가깝지만 불안 차원이 높음
        """
        return ModeConfig(
            gate_threshold=0.1,  # 낮은 임계값 (과각성)
            max_channels=2,  # 적은 채널 (집중)
            decision_temperature=6.0,  # 매우 높음 (강한 고착)
            working_memory_capacity=7,
            tau=0.05,  # 매우 낮음 (극도의 착취)
            impulsivity=0.2,  # 낮은 충동성
            patience=0.95,  # 매우 높은 인내심 (루틴 유지)
            damping=0.95,  # 매우 높은 감쇠 (기억 지속)
            local_weight_boost=4.0,  # 매우 높은 로컬 연결 (패턴 고착)
            novelty_sensitivity=4.0,  # 매우 높은 민감도 (변화 공포)
            stress_baseline=0.7,  # 높은 스트레스
        )
    
    @staticmethod
    def ied() -> ModeConfig:
        """
        분노조절장애 모드: 충동, 폭발적 분노
        
        특징:
        - 폭발적 분노
        - 극도의 충동성
        - 감정 조절 실패
        - ADHD 쪽 (높은 충동성)
        """
        return ModeConfig(
            gate_threshold=0.1,  # 낮은 임계값
            max_channels=10,  # 많은 채널
            decision_temperature=0.3,  # 매우 낮음 (충동적)
            working_memory_capacity=4,  # 낮음
            tau=2.5,  # 매우 높은 탐색
            impulsivity=0.95,  # 극도의 충동성
            patience=0.05,  # 극도로 낮은 인내심
            damping=0.85,
            local_weight_boost=0.8,  # 글로벌 연결 선호
            novelty_sensitivity=2.5,  # 높은 민감도
            stress_baseline=0.8,  # 매우 높은 스트레스
        )
    
    @staticmethod
    def depression() -> ModeConfig:
        """
        우울증 모드: 무기력, 부정적 편향
        
        특징:
        - 에너지 저하
        - 무기력
        - 부정적 인지 편향
        - ASD 쪽 (착취, 고착)
        """
        return ModeConfig(
            gate_threshold=0.4,  # 높은 임계값 (무기력)
            max_channels=2,  # 적은 채널
            decision_temperature=2.0,  # 높음 (고착)
            working_memory_capacity=5,
            tau=0.3,  # 낮음 (착취)
            impulsivity=0.2,  # 낮은 충동성
            patience=0.8,  # 높은 인내심 (하지만 부정적)
            damping=0.9,  # 높은 감쇠
            local_weight_boost=2.5,  # 로컬 연결 강화
            novelty_sensitivity=0.5,  # 낮은 민감도 (무기력)
            stress_baseline=0.6,  # 높은 스트레스
        )
    
    @staticmethod
    def bipolar_mania() -> ModeConfig:
        """
        양극성 장애 - 조증 상태
        
        특징:
        - 과도한 에너지
        - 높은 탐색
        - 충동성
        - ADHD 쪽
        """
        return ModeConfig(
            gate_threshold=0.05,  # 매우 낮음
            max_channels=15,  # 매우 많은 채널
            decision_temperature=0.3,  # 매우 낮음
            working_memory_capacity=5,
            tau=3.0,  # 극도의 탐색
            impulsivity=0.9,  # 높은 충동성
            patience=0.1,  # 낮은 인내심
            damping=0.85,
            local_weight_boost=0.5,  # 글로벌 연결 선호
            novelty_sensitivity=3.0,  # 높은 민감도
            stress_baseline=0.3,  # 낮은 스트레스 (조증)
        )
    
    @staticmethod
    def bipolar_depression() -> ModeConfig:
        """
        양극성 장애 - 우울 상태
        
        특징:
        - 에너지 저하
        - 낮은 탐색
        - 고착
        - ASD 쪽
        """
        return ModeConfig(
            gate_threshold=0.5,  # 높음
            max_channels=2,  # 적음
            decision_temperature=3.0,  # 높음
            working_memory_capacity=5,
            tau=0.2,  # 낮음
            impulsivity=0.2,  # 낮은 충동성
            patience=0.7,  # 높은 인내심
            damping=0.9,  # 높은 감쇠
            local_weight_boost=3.0,  # 로컬 연결 강화
            novelty_sensitivity=0.5,  # 낮은 민감도
            stress_baseline=0.7,  # 높은 스트레스
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
        elif mode == CognitiveMode.PANIC:
            return CognitiveModePresets.panic()
        elif mode == CognitiveMode.EPILEPSY:
            return CognitiveModePresets.epilepsy()
        elif mode == CognitiveMode.OCD:
            return CognitiveModePresets.ocd()
        elif mode == CognitiveMode.IED:
            return CognitiveModePresets.ied()
        elif mode == CognitiveMode.DEPRESSION:
            return CognitiveModePresets.depression()
        elif mode == CognitiveMode.BIPOLAR:
            return CognitiveModePresets.bipolar_mania()  # 기본값은 조증
        else:
            raise ValueError(f"Unknown mode: {mode}")

