#!/usr/bin/env python3
"""
치매/알츠하이머 동역학 향상된 테스트 스크립트

시간축 분리 효과를 명확히 보여주는 테스트

사용법:
    python test_dementia_alzheimer_enhanced.py
"""

import sys
import time
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cognitive_kernel import CognitiveKernel
from cognitive_kernel.cognitive_modes import CognitiveMode


def print_section(title: str):
    """섹션 제목 출력"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def simulate_old_memory(kernel, event_type: str, hours_ago: float):
    """오래된 기억 시뮬레이션 (timestamp 조작)"""
    # 실제로는 timestamp를 직접 설정할 수 없으므로,
    # 시간 경과 후 테스트하거나 다른 방법 사용
    # 여기서는 설명만 출력
    pass


def test_time_axis_separation():
    """시간축 분리 효과 명확히 보여주는 테스트"""
    print_section("⏰ 시간축 분리 효과 테스트")
    
    print("\n📌 핵심 개념:")
    print("   - 치매: 오래된 기억(1시간 이상) 감쇠, 새 기억 정상")
    print("   - 알츠하이머: 새 기억(1시간 미만) 즉시 감쇠, 오래된 기억 느리게 감쇠")
    print("   - 기억 나이 임계값: 3600초 (1시간)")
    
    # 치매 모드
    print("\n" + "-" * 60)
    print("1️⃣ 치매 모드 - 시간축 분리 효과")
    print("-" * 60)
    
    kernel_d = CognitiveKernel('test_dementia_time_axis', mode=CognitiveMode.DEMENTIA)
    
    print(f"\n파라미터:")
    print(f"   old_memory_decay_rate: {kernel_d.dynamics.config.old_memory_decay_rate}")
    print(f"   new_memory_decay_rate: {kernel_d.dynamics.config.new_memory_decay_rate}")
    print(f"   memory_age_threshold: {kernel_d.dynamics.config.memory_age_threshold}초")
    
    # 기억 저장
    print(f"\n기억 저장:")
    kernel_d.remember("old_memory", {"content": "오래된 기억 (2시간 전)"}, importance=0.9)
    time.sleep(0.1)
    kernel_d.remember("new_memory", {"content": "새 기억 (방금)"}, importance=0.9)
    
    # 기억 회상
    memories_d = kernel_d.recall(k=5)
    current_time = time.time()
    
    print(f"\n기억 회상 결과:")
    total_importance_before = 0.0
    total_importance_after = 0.0
    
    for m in memories_d:
        timestamp = m.get('timestamp', current_time)
        age = current_time - timestamp
        importance_before = 0.9  # 원래 importance
        importance_after = m.get('importance', 0.0)
        
        total_importance_before += importance_before
        total_importance_after += importance_after
        
        if age > 3600:
            decay_factor = math.exp(-kernel_d.dynamics.config.old_memory_decay_rate * age)
            print(f"   {m.get('event_type')}: age={age/3600:.2f}시간 (오래된 기억)")
            print(f"      원래 importance: {importance_before:.3f}")
            print(f"      감쇠 후 importance: {importance_after:.3f}")
            print(f"      감쇠율: {decay_factor:.6f}")
        else:
            print(f"   {m.get('event_type')}: age={age:.1f}초 (새 기억)")
            print(f"      원래 importance: {importance_before:.3f}")
            print(f"      감쇠 후 importance: {importance_after:.3f} (정상, 감쇠 없음)")
    
    # 코어 강도
    core_d = kernel_d.dynamics.calculate_core_strength(memories_d)
    print(f"\n코어 강도:")
    print(f"   총 importance (감쇠 전): {total_importance_before:.3f}")
    print(f"   총 importance (감쇠 후): {total_importance_after:.3f}")
    print(f"   Core Strength: {core_d:.3f}")
    
    # 알츠하이머 모드
    print("\n" + "-" * 60)
    print("2️⃣ 알츠하이머 모드 - 시간축 분리 효과")
    print("-" * 60)
    
    kernel_a = CognitiveKernel('test_alzheimer_time_axis', mode=CognitiveMode.ALZHEIMER)
    
    print(f"\n파라미터:")
    print(f"   old_memory_decay_rate: {kernel_a.dynamics.config.old_memory_decay_rate}")
    print(f"   new_memory_decay_rate: {kernel_a.dynamics.config.new_memory_decay_rate}")
    print(f"   memory_age_threshold: {kernel_a.dynamics.config.memory_age_threshold}초")
    
    # 기억 저장
    print(f"\n기억 저장:")
    kernel_a.remember("old_memory", {"content": "오래된 기억 (2시간 전)"}, importance=0.9)
    time.sleep(0.1)
    kernel_a.remember("new_memory", {"content": "새 기억 (방금)"}, importance=0.9)
    
    # 기억 회상
    memories_a = kernel_a.recall(k=5)
    
    print(f"\n기억 회상 결과:")
    total_importance_before_a = 0.0
    total_importance_after_a = 0.0
    
    for m in memories_a:
        timestamp = m.get('timestamp', current_time)
        age = current_time - timestamp
        importance_before = 0.9
        importance_after = m.get('importance', 0.0)
        
        total_importance_before_a += importance_before
        total_importance_after_a += importance_after
        
        if age > 3600:
            decay_factor = math.exp(-kernel_a.dynamics.config.old_memory_decay_rate * age)
            print(f"   {m.get('event_type')}: age={age/3600:.2f}시간 (오래된 기억)")
            print(f"      원래 importance: {importance_before:.3f}")
            print(f"      감쇠 후 importance: {importance_after:.3f}")
            print(f"      감쇠율: {decay_factor:.6f} (느림)")
        else:
            decay_factor = math.exp(-kernel_a.dynamics.config.new_memory_decay_rate * age)
            print(f"   {m.get('event_type')}: age={age:.1f}초 (새 기억)")
            print(f"      원래 importance: {importance_before:.3f}")
            print(f"      감쇠 후 importance: {importance_after:.3f}")
            print(f"      감쇠율: {decay_factor:.6f} (매우 빠름, 알츠하이머 특성)")
    
    # 코어 강도
    core_a = kernel_a.dynamics.calculate_core_strength(memories_a)
    print(f"\n코어 강도:")
    print(f"   총 importance (감쇠 전): {total_importance_before_a:.3f}")
    print(f"   총 importance (감쇠 후): {total_importance_after_a:.3f}")
    print(f"   Core Strength: {core_a:.3f}")
    
    # 비교
    print("\n" + "-" * 60)
    print("3️⃣ 비교")
    print("-" * 60)
    print(f"\n치매 vs 알츠하이머:")
    print(f"   치매 Core Strength: {core_d:.3f}")
    print(f"   알츠하이머 Core Strength: {core_a:.3f}")
    print(f"   차이: {abs(core_d - core_a):.3f}")
    
    print(f"\n💡 핵심 차이:")
    print(f"   - 치매: 새 기억은 정상 유지, 오래된 기억만 느리게 감쇠")
    print(f"   - 알츠하이머: 새 기억이 즉시 감쇠, 오래된 기억은 느리게 감쇠")
    print(f"   - 알츠하이머의 새 기억 감쇠율(0.1)은 치매의 오래된 기억 감쇠율(0.0001)보다 1000배 빠름")


def main():
    """메인 함수"""
    print("=" * 60)
    print("  🧠 치매/알츠하이머 시간축 분리 효과 테스트")
    print("=" * 60)
    print(f"\n버전: v2.0.2")
    print(f"날짜: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        test_time_axis_separation()
        
        print_section("✅ 테스트 완료")
        print("\n📝 참고:")
        print("   - 실제 시간축 분리 효과를 보려면 1시간 이상 경과한 기억이 필요합니다")
        print("   - 현재 테스트는 짧은 시간 차이로 인해 효과가 제한적입니다")
        print("   - 알츠하이머의 새 기억 감쇠는 매우 빠르므로(0.1), 몇 초만 지나도 감쇠가 시작됩니다")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

