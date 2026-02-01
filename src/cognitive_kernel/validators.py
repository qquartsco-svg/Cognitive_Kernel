"""
입력 검증 유틸리티

산업용/연구용 기준으로 엄격한 타입 및 범위 검증
"""

from typing import Any, Dict, List, Optional
from .exceptions import ValidationError


def validate_importance(importance: float, param_name: str = "importance") -> None:
    """
    importance 값 검증 (0.0 ~ 1.0)
    
    Args:
        importance: 검증할 값
        param_name: 파라미터 이름 (에러 메시지용)
    
    Raises:
        ValidationError: 범위를 벗어난 경우
    """
    if not isinstance(importance, (int, float)):
        raise ValidationError(
            f"{param_name} must be numeric, got {type(importance).__name__}"
        )
    
    if importance < 0.0 or importance > 1.0:
        raise ValidationError(
            f"{param_name} must be in range [0.0, 1.0], got {importance}"
        )


def validate_emotion(emotion: float, param_name: str = "emotion") -> None:
    """
    emotion 값 검증 (0.0 ~ 1.0)
    
    Args:
        emotion: 검증할 값
        param_name: 파라미터 이름 (에러 메시지용)
    
    Raises:
        ValidationError: 범위를 벗어난 경우
    """
    if not isinstance(emotion, (int, float)):
        raise ValidationError(
            f"{param_name} must be numeric, got {type(emotion).__name__}"
        )
    
    if emotion < 0.0 or emotion > 1.0:
        raise ValidationError(
            f"{param_name} must be in range [0.0, 1.0], got {emotion}"
        )


def validate_k(k: int, param_name: str = "k") -> None:
    """
    k 값 검증 (양의 정수)
    
    Args:
        k: 검증할 값
        param_name: 파라미터 이름 (에러 메시지용)
    
    Raises:
        ValidationError: 범위를 벗어난 경우
    """
    if not isinstance(k, int):
        raise ValidationError(
            f"{param_name} must be integer, got {type(k).__name__}"
        )
    
    if k <= 0:
        raise ValidationError(
            f"{param_name} must be positive integer, got {k}"
        )


def validate_options(options: List[str], param_name: str = "options") -> None:
    """
    options 리스트 검증
    
    Args:
        options: 검증할 리스트
        param_name: 파라미터 이름 (에러 메시지용)
    
    Raises:
        ValidationError: 유효하지 않은 경우
    """
    if not isinstance(options, list):
        raise ValidationError(
            f"{param_name} must be list, got {type(options).__name__}"
        )
    
    if len(options) == 0:
        raise ValidationError(
            f"{param_name} must not be empty"
        )
    
    for i, opt in enumerate(options):
        if not isinstance(opt, str):
            raise ValidationError(
                f"{param_name}[{i}] must be string, got {type(opt).__name__}"
            )
        if len(opt.strip()) == 0:
            raise ValidationError(
                f"{param_name}[{i}] must not be empty string"
            )


def validate_timestamp(timestamp: float, param_name: str = "timestamp") -> None:
    """
    timestamp 값 검증 (유효한 Unix timestamp)
    
    Args:
        timestamp: 검증할 값
        param_name: 파라미터 이름 (에러 메시지용)
    
    Raises:
        ValidationError: 유효하지 않은 경우
    """
    if not isinstance(timestamp, (int, float)):
        raise ValidationError(
            f"{param_name} must be numeric, got {type(timestamp).__name__}"
        )
    
    # 합리적인 범위: 1970-01-01 ~ 2100-01-01
    MIN_TIMESTAMP = 0.0
    MAX_TIMESTAMP = 4102444800.0  # 2100-01-01 00:00:00 UTC
    
    if timestamp < MIN_TIMESTAMP or timestamp > MAX_TIMESTAMP:
        raise ValidationError(
            f"{param_name} must be valid Unix timestamp "
            f"({MIN_TIMESTAMP} ~ {MAX_TIMESTAMP}), got {timestamp}"
        )


def validate_event_type(event_type: str, param_name: str = "event_type") -> None:
    """
    event_type 문자열 검증
    
    Args:
        event_type: 검증할 문자열
        param_name: 파라미터 이름 (에러 메시지용)
    
    Raises:
        ValidationError: 유효하지 않은 경우
    """
    if not isinstance(event_type, str):
        raise ValidationError(
            f"{param_name} must be string, got {type(event_type).__name__}"
        )
    
    if len(event_type.strip()) == 0:
        raise ValidationError(
            f"{param_name} must not be empty string"
        )


def validate_content(content: Optional[Dict[str, Any]], param_name: str = "content") -> None:
    """
    content 딕셔너리 검증
    
    Args:
        content: 검증할 딕셔너리 (None 허용)
        param_name: 파라미터 이름 (에러 메시지용)
    
    Raises:
        ValidationError: 유효하지 않은 경우
    """
    if content is not None and not isinstance(content, dict):
        raise ValidationError(
            f"{param_name} must be dict or None, got {type(content).__name__}"
        )


def validate_related_to(related_to: Optional[List[str]], param_name: str = "related_to") -> None:
    """
    related_to 리스트 검증
    
    Args:
        related_to: 검증할 리스트 (None 허용)
        param_name: 파라미터 이름 (에러 메시지용)
    
    Raises:
        ValidationError: 유효하지 않은 경우
    """
    if related_to is not None:
        if not isinstance(related_to, list):
            raise ValidationError(
                f"{param_name} must be list or None, got {type(related_to).__name__}"
            )
        
        for i, item in enumerate(related_to):
            if not isinstance(item, str):
                raise ValidationError(
                    f"{param_name}[{i}] must be string, got {type(item).__name__}"
                )

