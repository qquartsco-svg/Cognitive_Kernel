"""
API 계약 테스트

산업용/연구용 기준으로 스펙 기반 테스트 작성
"""

import pytest
import sys
from pathlib import Path

# 프로젝트 루트를 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from cognitive_kernel import CognitiveKernel, CognitiveMode
from cognitive_kernel.exceptions import (
    ValidationError,
    ModeError,
    DecisionError,
)


class TestRememberContract:
    """remember() API 계약 테스트"""
    
    def test_remember_valid_inputs(self):
        """정상 입력 테스트"""
        kernel = CognitiveKernel()
        
        # 기본 사용
        event_id = kernel.remember("test", importance=0.5)
        assert isinstance(event_id, str)
        assert len(event_id) > 0
        
        # content 포함
        event_id = kernel.remember("test", content={"key": "value"}, importance=0.9)
        assert isinstance(event_id, str)
        
        # 경계값: importance=0.0
        event_id = kernel.remember("test", importance=0.0)
        assert isinstance(event_id, str)
        
        # 경계값: importance=1.0
        event_id = kernel.remember("test", importance=1.0)
        assert isinstance(event_id, str)
    
    def test_remember_invalid_importance(self):
        """importance 범위 검증"""
        kernel = CognitiveKernel()
        
        # 음수
        with pytest.raises(ValidationError, match="importance must be in range"):
            kernel.remember("test", importance=-0.1)
        
        # 1.0 초과
        with pytest.raises(ValidationError, match="importance must be in range"):
            kernel.remember("test", importance=1.1)
    
    def test_remember_invalid_event_type(self):
        """event_type 검증"""
        kernel = CognitiveKernel()
        
        # 빈 문자열
        with pytest.raises(ValidationError, match="event_type must not be empty"):
            kernel.remember("", importance=0.5)
        
        # 공백만
        with pytest.raises(ValidationError, match="event_type must not be empty"):
            kernel.remember("   ", importance=0.5)
    
    def test_remember_invalid_emotion(self):
        """emotion 범위 검증"""
        kernel = CognitiveKernel()
        
        # 음수
        with pytest.raises(ValidationError, match="emotion must be in range"):
            kernel.remember("test", emotion=-0.1)
        
        # 1.0 초과
        with pytest.raises(ValidationError, match="emotion must be in range"):
            kernel.remember("test", emotion=1.1)
    
    def test_remember_invalid_content(self):
        """content 타입 검증"""
        kernel = CognitiveKernel()
        
        # dict가 아닌 타입
        with pytest.raises(ValidationError, match="content must be dict or None"):
            kernel.remember("test", content="not a dict")
        
        # None은 허용
        event_id = kernel.remember("test", content=None)
        assert isinstance(event_id, str)


class TestRecallContract:
    """recall() API 계약 테스트"""
    
    def test_recall_valid_inputs(self):
        """정상 입력 테스트"""
        kernel = CognitiveKernel()
        
        # 기본 사용
        memories = kernel.recall(k=5)
        assert isinstance(memories, list)
        
        # k=1
        memories = kernel.recall(k=1)
        assert isinstance(memories, list)
    
    def test_recall_invalid_k(self):
        """k 범위 검증"""
        kernel = CognitiveKernel()
        
        # k=0
        with pytest.raises(ValidationError, match="k must be positive integer"):
            kernel.recall(k=0)
        
        # k=-1
        with pytest.raises(ValidationError, match="k must be positive integer"):
            kernel.recall(k=-1)
    
    def test_recall_output_schema(self):
        """출력 스키마 검증"""
        kernel = CognitiveKernel()
        
        # 기억 추가
        kernel.remember("test1", importance=0.9)
        kernel.remember("test2", importance=0.8)
        
        memories = kernel.recall(k=2)
        
        # 빈 리스트 또는 필수 필드 확인
        if len(memories) > 0:
            memory = memories[0]
            assert "id" in memory
            assert "event_type" in memory
            assert "content" in memory
            assert "importance" in memory
            assert "timestamp" in memory
            
            # 타입 확인
            assert isinstance(memory["id"], str)
            assert isinstance(memory["event_type"], str)
            assert isinstance(memory["content"], dict)
            assert isinstance(memory["importance"], float)
            assert isinstance(memory["timestamp"], float)
            
            # 범위 확인
            assert 0.0 <= memory["importance"] <= 1.0


class TestDecideContract:
    """decide() API 계약 테스트"""
    
    def test_decide_valid_inputs(self):
        """정상 입력 테스트"""
        kernel = CognitiveKernel()
        
        # 기본 사용
        result = kernel.decide(["rest", "work", "exercise"])
        assert isinstance(result, dict)
        
        # 1개 옵션
        result = kernel.decide(["rest"])
        assert isinstance(result, dict)
    
    def test_decide_invalid_options(self):
        """options 검증"""
        kernel = CognitiveKernel()
        
        # 빈 리스트
        with pytest.raises(ValidationError, match="options must not be empty"):
            kernel.decide([])
        
        # 빈 문자열 포함
        with pytest.raises(ValidationError, match="options.*must not be empty string"):
            kernel.decide(["", "work"])
        
        # 공백만 포함
        with pytest.raises(ValidationError, match="options.*must not be empty string"):
            kernel.decide(["   ", "work"])
    
    def test_decide_output_schema(self):
        """출력 스키마 검증"""
        kernel = CognitiveKernel()
        
        # 기억 추가 (결과가 더 안정적이 되도록)
        kernel.remember("test1", importance=0.9)
        kernel.remember("test2", importance=0.8)
        
        result = kernel.decide(["rest", "work", "exercise"])
        
        # 필수 키 확인
        assert "action" in result
        assert "utility" in result
        assert "probability" in result
        assert "probability_distribution" in result
        assert "entropy" in result
        assert "core_strength" in result
        
        # 타입 확인
        assert result["action"] is None or isinstance(result["action"], str)
        assert isinstance(result["utility"], float)
        assert isinstance(result["probability"], float)
        assert isinstance(result["probability_distribution"], dict)
        assert isinstance(result["entropy"], float)
        assert isinstance(result["core_strength"], float)
        
        # 확률 분포 정규화 확인
        prob_dist = result["probability_distribution"]
        assert len(prob_dist) > 0, "probability_distribution should not be empty"
        prob_sum = sum(prob_dist.values())
        assert abs(prob_sum - 1.0) < 1e-6, f"Probability sum should be 1.0, got {prob_sum}"
        
        # 범위 확인
        assert 0.0 <= result["core_strength"] <= 1.0


class TestSetModeContract:
    """set_mode() API 계약 테스트"""
    
    def test_set_mode_enum(self):
        """enum 모드 테스트"""
        kernel = CognitiveKernel()
        
        # 정상 enum
        kernel.set_mode(CognitiveMode.ADHD)
        assert kernel.mode == CognitiveMode.ADHD
        
        kernel.set_mode(CognitiveMode.ASD)
        assert kernel.mode == CognitiveMode.ASD
    
    def test_set_mode_string(self):
        """문자열 모드 테스트 (대소문자 무시)"""
        kernel = CognitiveKernel()
        
        # 소문자
        kernel.set_mode("adhd")
        assert kernel.mode == CognitiveMode.ADHD
        
        # 대문자
        kernel.set_mode("ASD")
        assert kernel.mode == CognitiveMode.ASD
        
        # 혼합
        kernel.set_mode("Dementia")
        assert kernel.mode == CognitiveMode.DEMENTIA
        
        # 공백 제거
        kernel.set_mode("  alzheimer  ")
        assert kernel.mode == CognitiveMode.ALZHEIMER
    
    def test_set_mode_invalid(self):
        """잘못된 모드 테스트"""
        kernel = CognitiveKernel()
        
        # 잘못된 모드
        with pytest.raises(ModeError, match="Invalid mode"):
            kernel.set_mode("INVALID_MODE")
        
        # 잘못된 타입
        with pytest.raises(ModeError, match="mode must be CognitiveMode enum or string"):
            kernel.set_mode(123)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

