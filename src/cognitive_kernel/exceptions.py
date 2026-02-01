"""
Cognitive Kernel 예외 클래스

산업용/연구용 엔지니어링 기준으로 명확한 예외 타입 정의
"""


class CognitiveKernelError(Exception):
    """Cognitive Kernel 기본 예외"""
    pass


class ValidationError(CognitiveKernelError):
    """입력 검증 실패"""
    pass


class ConfigurationError(CognitiveKernelError):
    """설정 오류"""
    pass


class MemoryError(CognitiveKernelError):
    """메모리 관련 오류"""
    pass


class DecisionError(CognitiveKernelError):
    """의사결정 관련 오류"""
    pass


class ModeError(CognitiveKernelError):
    """인지 모드 관련 오류"""
    pass

