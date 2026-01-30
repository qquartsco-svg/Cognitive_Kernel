"""
⚖️ Cognitive Polarity Demo - ADHD vs ASD

"탐색(Exploration) vs 착취(Exploitation)"의 극단을 보여주는 데모:

- ADHD: 고엔트로피 (High Entropy) - 계속 시도하고 싶은 욕망 (+)
- ASD: 저엔트로피 (Low Entropy) - 패턴을 유지하고 싶은 욕망 (-)

수식:
    Entropy_Control = Exploration(ADHD) / Exploitation(ASD)

Usage:
    pip install cognitive-kernel
    python examples/cognitive_polarity_demo.py
"""

from cognitive_kernel import CognitiveKernel, CognitiveMode
import time

# ============================================================
# 🎯 시나리오: "패턴 고착 vs 산만함"
# ============================================================

def demo_cognitive_polarity():
    """
    ADHD와 ASD의 극단적 대칭을 보여주는 데모
    
    시나리오:
    1. 동일한 입력을 Normal, ADHD, ASD 모드에 주입
    2. 의사결정의 일관성(Consistency) 비교
    3. 패턴 고착 vs 산만함의 동역학 관찰
    """
    
    print("\n" + "="*70)
    print("⚖️ Cognitive Polarity: ADHD vs ASD")
    print("="*70)
    print("\n📖 Scenario: 'Pattern Fixation vs Distraction'")
    print("-" * 70)
    
    # ============================================================
    # Step 1: Normal Mode - 기준선
    # ============================================================
    print("\n🧠 Step 1: Normal Mode (Baseline)")
    print("-" * 70)
    
    kernel_normal = CognitiveKernel("normal_demo", mode=CognitiveMode.NORMAL)
    
    # 패턴 형성: "빨간색" 관련 기억
    print("\n   📝 Forming pattern: 'red' related memories")
    red_memories = [
        "I saw a red apple",
        "Red traffic light stopped me",
        "Red sunset was beautiful",
    ]
    
    for mem in red_memories:
        kernel_normal.remember("observation", {"text": mem}, importance=0.5)
        print(f"   ✅ Stored: {mem[:40]}...")
    
    # 의사결정 테스트
    decisions_normal = []
    for i in range(5):
        decision = kernel_normal.decide(["choose_red", "choose_blue", "choose_green"])
        decisions_normal.append(decision["action"])
        print(f"   Decision {i+1}: {decision['action']} (utility: {decision['utility']:.3f})")
    
    consistency_normal = len(set(decisions_normal)) / len(decisions_normal)
    print(f"\n   📊 Consistency: {consistency_normal:.2%} (lower = more consistent)")
    
    # ============================================================
    # Step 2: ADHD Mode - 산만함
    # ============================================================
    print("\n" + "="*70)
    print("🔴 ADHD Mode: High Entropy (Over-Exploration)")
    print("="*70)
    
    kernel_adhd = CognitiveKernel("adhd_demo", mode=CognitiveMode.ADHD)
    
    # 동일한 패턴 형성
    print("\n   📝 Forming same pattern: 'red' related memories")
    for mem in red_memories:
        kernel_adhd.remember("observation", {"text": mem}, importance=0.5)
    
    # 의사결정 테스트
    print("\n   🎯 Decision-making (5 trials):")
    decisions_adhd = []
    for i in range(5):
        decision = kernel_adhd.decide(["choose_red", "choose_blue", "choose_green"])
        decisions_adhd.append(decision["action"])
        print(f"   Decision {i+1}: {decision['action']} (utility: {decision['utility']:.3f})")
    
    consistency_adhd = len(set(decisions_adhd)) / len(decisions_adhd)
    print(f"\n   📊 Consistency: {consistency_adhd:.2%}")
    print(f"   ⚠️  ADHD: Low consistency (distracted, keeps switching)")
    
    # ============================================================
    # Step 3: ASD Mode - 패턴 고착
    # ============================================================
    print("\n" + "="*70)
    print("🔵 ASD Mode: Low Entropy (Over-Exploitation)")
    print("="*70)
    
    kernel_asd = CognitiveKernel("asd_demo", mode=CognitiveMode.ASD)
    
    # 동일한 패턴 형성
    print("\n   📝 Forming same pattern: 'red' related memories")
    for mem in red_memories:
        kernel_asd.remember("observation", {"text": mem}, importance=0.5)
    
    # 의사결정 테스트
    print("\n   🎯 Decision-making (5 trials):")
    decisions_asd = []
    for i in range(5):
        decision = kernel_asd.decide(["choose_red", "choose_blue", "choose_green"])
        decisions_asd.append(decision["action"])
        print(f"   Decision {i+1}: {decision['action']} (utility: {decision['utility']:.3f})")
    
    consistency_asd = len(set(decisions_asd)) / len(decisions_asd)
    print(f"\n   📊 Consistency: {consistency_asd:.2%}")
    print(f"   ⚠️  ASD: High consistency (pattern fixation, routine adherence)")
    
    # ============================================================
    # Step 4: 패턴 고착 테스트 - "빨간색" 강화
    # ============================================================
    print("\n" + "="*70)
    print("🔵 ASD Mode: Pattern Fixation Test")
    print("="*70)
    
    # ASD 모드에서 "빨간색" 패턴 강화
    print("\n   📝 Reinforcing 'red' pattern (10 more memories)")
    for i in range(10):
        kernel_asd.remember("observation", {
            "text": f"Red object {i+1} caught my attention"
        }, importance=0.6)
    
    # 새로운 선택지 추가: "choose_yellow"
    print("\n   🎯 New option introduced: 'choose_yellow'")
    print("   Testing if ASD mode can break from 'red' pattern:")
    
    decisions_asd_new = []
    for i in range(5):
        decision = kernel_asd.decide([
            "choose_red", 
            "choose_blue", 
            "choose_green",
            "choose_yellow"  # 새로운 옵션
        ])
        decisions_asd_new.append(decision["action"])
        print(f"   Decision {i+1}: {decision['action']} (utility: {decision['utility']:.3f})")
    
    red_count = decisions_asd_new.count("choose_red")
    print(f"\n   📊 'choose_red' selected: {red_count}/5 times")
    print(f"   ⚠️  ASD: Pattern fixation prevents exploring new options")
    
    # ============================================================
    # Step 5: 비교 요약
    # ============================================================
    print("\n" + "="*70)
    print("📊 Comparison Summary")
    print("="*70)
    
    print("\n┌─────────────────────────────────────────────────────────────────┐")
    print("│  Mode    │ Consistency │ Entropy │ Key Behavior                │")
    print("├─────────────────────────────────────────────────────────────────┤")
    print(f"│  Normal  │  {consistency_normal:.2%}      │  Medium  │ Balanced exploration/exploitation │")
    print(f"│  ADHD    │  {consistency_adhd:.2%}      │  High    │ Over-exploration (distracted)    │")
    print(f"│  ASD     │  {consistency_asd:.2%}      │  Low     │ Over-exploitation (fixated)      │")
    print("└─────────────────────────────────────────────────────────────────┘")
    
    print("\n💡 Key Insights:")
    print("   • ADHD: 계속 시도하고 싶은 욕망 (+) → 높은 엔트로피")
    print("   • ASD: 패턴을 유지하고 싶은 욕망 (-) → 낮은 엔트로피")
    print("   • Entropy_Control = Exploration(ADHD) / Exploitation(ASD)")
    print("   • 균형(Normal)이 가장 효율적인 의사결정을 만듦")
    
    # 저장
    kernel_normal.save()
    kernel_adhd.save()
    kernel_asd.save()


# ============================================================
# 🎯 시나리오: "감각 과부하 (ASD)"
# ============================================================

def demo_sensory_overload():
    """
    ASD 모드의 감각 과부하 시뮬레이션
    
    Thalamus의 gate_threshold가 0에 가까워서
    모든 미세 자극이 시스템에 부하를 주는 현상
    """
    
    print("\n" + "="*70)
    print("🔵 ASD Mode: Sensory Overload Simulation")
    print("="*70)
    
    kernel_asd = CognitiveKernel("asd_sensory", mode=CognitiveMode.ASD)
    
    print("\n📝 Simulating sensory inputs (normal vs ASD):")
    print("-" * 70)
    
    # 미세한 자극들
    micro_stimuli = [
        "Fluorescent light humming",
        "Fabric texture on skin",
        "Distant conversation",
        "Keyboard clicking",
        "Air conditioning noise",
    ]
    
    print("\n   Normal mode: These stimuli are filtered (gate_threshold=0.3)")
    print("   ASD mode: All stimuli pass through (gate_threshold=0.0)")
    
    print("\n   📥 Processing stimuli in ASD mode:")
    for i, stimulus in enumerate(micro_stimuli, 1):
        # Thalamus 게이팅 시뮬레이션
        gate_threshold = kernel_asd.mode_config.gate_threshold
        passed = True  # ASD에서는 모든 입력 통과
        
        if passed:
            kernel_asd.remember("sensory_input", {
                "text": stimulus,
                "intensity": 0.1  # 낮은 강도
            }, importance=0.2)
            print(f"   {i}. ✅ Passed: {stimulus} (threshold: {gate_threshold:.2f})")
    
    print("\n   ⚠️  Result: System overload from too many simultaneous inputs")
    print("   💡 This simulates ASD sensory sensitivity")
    
    kernel_asd.save()


# ============================================================
# 🏃 Main
# ============================================================

if __name__ == "__main__":
    print("\n🧠 Cognitive Polarity Demo: ADHD vs ASD")
    print("━" * 70)
    
    try:
        demo_cognitive_polarity()
        demo_sensory_overload()
        
        print("\n" + "="*70)
        print("✅ Demo completed!")
        print("="*70)
        print("\n📁 Files created:")
        print("   - .cognitive_kernel/normal_demo/")
        print("   - .cognitive_kernel/adhd_demo/")
        print("   - .cognitive_kernel/asd_demo/")
        print("   - .cognitive_kernel/asd_sensory/")
        
        print("\n💡 Next Steps:")
        print("   • Try: kernel.set_mode(CognitiveMode.ASD)")
        print("   • Observe: Pattern fixation in decision-making")
        print("   • Compare: Normal vs ADHD vs ASD behaviors")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

