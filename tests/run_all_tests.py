#!/usr/bin/env python3
"""
통합 테스트 실행 스크립트

모든 테스트를 한 번에 실행합니다.
"""

import sys
import subprocess
from pathlib import Path

def run_tests():
    """모든 테스트 실행"""
    test_dir = Path(__file__).parent
    
    print("=" * 60)
    print("Cognitive Kernel 통합 테스트 실행")
    print("=" * 60)
    
    # pytest로 실행
    try:
        result = subprocess.run(
            ["python", "-m", "pytest", str(test_dir), "-v"],
            cwd=test_dir.parent,
            capture_output=False
        )
        return result.returncode == 0
    except FileNotFoundError:
        print("⚠️  pytest가 설치되지 않았습니다.")
        print("   설치: pip install pytest")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

