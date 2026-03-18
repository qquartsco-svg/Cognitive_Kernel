"""
🧠 Cognitive Kernel
==================

AI 에이전트를 위한 최소 검증 가능한(Minimal, Verifiable) 장기 기억 시스템

Features:
- 진짜 장기 기억 (영속성)
- 자동 세션 관리 (with 문 지원)
- 7개 인지 엔진 통합
- Edge AI First 설계

Quick Start:
    from cognitive_kernel import CognitiveKernel
    
    with CognitiveKernel("my_brain") as kernel:
        kernel.remember("meeting", {"topic": "project"}, importance=0.9)
        memories = kernel.recall(k=5)
        decision = kernel.decide(["rest", "work", "exercise"])
    # 자동 저장됨

Author: GNJz (Qquarts)
License: MIT
"""

__version__ = "2.0.3"
__author__ = "GNJz (Qquarts)"

from .core import (
    CognitiveKernel,
    CognitiveConfig,
    create_kernel,
)
from .cognitive_modes import (
    CognitiveMode,
    CognitiveModePresets,
    ModeConfig,
)

# 엔진 접근 (고급 사용자용)
from .engines import (
    PanoramaMemoryEngine,
    PanoramaConfig,
    MemoryRankEngine,
    MemoryRankConfig,
    MemoryNodeAttributes,
    PFCEngine,
    PFCConfig,
    Action,
    BasalGangliaEngine,
    BasalGangliaConfig,
    DynamicsEngine,
    DynamicsConfig,
    DynamicsState,
    ContinuousDynamicsConfig,
    NeuralDynamicsCore,
    HebbianPlasticityConfig,
    hebbian_update,
    IrrationalAlgebraEngine,
    IrrationalAlgebraConfig,
    IrrationalAlgebraSnapshot,
    IrrationalConstant,
    IrrationalObservation,
    AlgebraicInvariant,
)

# Vector DB 통합 (선택적)
try:
    from .vector_integration import VectorDBBackend
    VECTOR_DB_AVAILABLE = True
except ImportError:
    VECTOR_DB_AVAILABLE = False
    VectorDBBackend = None

__all__ = [
    # 메인 클래스
    "CognitiveKernel",
    "CognitiveConfig",
    "create_kernel",
    # 버전
    "__version__",
    "__author__",
    # 인지 모드
    "CognitiveMode",
    "CognitiveModePresets",
    "ModeConfig",
    # 엔진 (고급)
    "PanoramaMemoryEngine",
    "PanoramaConfig",
    "MemoryRankEngine",
    "MemoryRankConfig",
    "MemoryNodeAttributes",
    "PFCEngine",
    "PFCConfig",
    "Action",
    "BasalGangliaEngine",
    "BasalGangliaConfig",
    "DynamicsEngine",
    "DynamicsConfig",
    "DynamicsState",
    "ContinuousDynamicsConfig",
    "NeuralDynamicsCore",
    "HebbianPlasticityConfig",
    "hebbian_update",
    "IrrationalAlgebraEngine",
    "IrrationalAlgebraConfig",
    "IrrationalAlgebraSnapshot",
    "IrrationalConstant",
    "IrrationalObservation",
    "AlgebraicInvariant",
    # Vector DB
    "VectorDBBackend",
    "VECTOR_DB_AVAILABLE",
]
