"""
⚡ Why Hybrid Memory Matters - Real Example

"The Forgotten Preference Revival" 시나리오:

과거에 낮은 중요도로 저장된 선호도가,
수많은 다른 기억들 사이에 묻혔다가,
Hybrid Cognitive Kernel에 의해 다시 회상되어
실제 의사결정을 바꾸는 순간을 증명합니다.

Usage:
    pip install cognitive-kernel chromadb sentence-transformers
    python examples/hybrid_failure_vs_success.py
"""

from cognitive_kernel import CognitiveKernel, VectorDBBackend
import time

# ============================================================
# 🎯 시나리오: "The Forgotten Preference Revival"
# ============================================================

def scenario_forgotten_preference():
    """
    시나리오:
    1. Day 1: 사용자가 "I hate morning meetings" (importance=0.2, 낮음)
    2. Day 2-10: 수십 개의 다른 기억들이 추가됨
    3. 현재: "schedule a meeting" 쿼리
    4. 결과 비교: Vector DB only vs Hybrid Cognitive Kernel
    """
    
    print("\n" + "="*70)
    print("⚡ Why Hybrid Memory Matters - Real Example")
    print("="*70)
    print("\n📖 Scenario: 'The Forgotten Preference Revival'")
    print("-" * 70)
    
    # ============================================================
    # Step 1: 초기 설정
    # ============================================================
    print("\n🔧 Step 1: Initialize Systems")
    print("-" * 70)
    
    # Vector DB only (비교용)
    vector_only = VectorDBBackend(
        backend_type="chroma",
        path="./chroma_vector_only",
        collection_name="vector_memory"
    )
    
    # Hybrid: Vector DB + Cognitive Kernel
    vector_hybrid = VectorDBBackend(
        backend_type="chroma",
        path="./chroma_hybrid",
        collection_name="hybrid_memory"
    )
    kernel_hybrid = CognitiveKernel("hybrid_demo")
    
    print("   ✅ Vector DB only system initialized")
    print("   ✅ Hybrid (Vector DB + Cognitive Kernel) system initialized")
    
    # ============================================================
    # Step 2: Day 1 - 중요한 선호도 저장 (낮은 중요도)
    # ============================================================
    print("\n📅 Day 1: Store Critical Preference (Low Initial Importance)")
    print("-" * 70)
    
    preference_text = "I hate morning meetings. They make me unproductive."
    
    # Hybrid: Cognitive Kernel에 먼저 저장 (실제 ID 받기)
    preference_id = kernel_hybrid.remember(
        event_type="preference",
        content={"text": preference_text},
        importance=0.2  # 낮은 중요도
    )
    
    # Vector DB only
    vector_only.add_memory(
        memory_id=preference_id,
        text=preference_text,
        metadata={"event_type": "preference", "day": 1},
        importance=0.2  # 낮은 중요도
    )
    
    # Hybrid: Vector DB에도 저장 (같은 ID 사용)
    vector_hybrid.add_memory(
        memory_id=preference_id,
        text=preference_text,
        metadata={"event_type": "preference", "day": 1},
        importance=0.2
    )
    
    print(f"   📝 Stored: '{preference_text[:40]}...'")
    print(f"   ⚠️  Initial importance: 0.2 (low)")
    
    # ============================================================
    # Step 2.5: Day 3, 5, 7 - 선호도 관련 이벤트 반복 (중요도 증가)
    # ============================================================
    print("\n📅 Day 3, 5, 7: Related Events (Importance Increases via MemoryRank)")
    print("-" * 70)
    
    related_events = [
        "Morning meeting was terrible, couldn't focus",
        "Had to reschedule morning meeting to afternoon",
        "Team agreed afternoon meetings work better"
    ]
    
    for i, event_text in enumerate(related_events):
        day = [3, 5, 7][i]
        
        # Hybrid: Cognitive Kernel에 저장 (preference와 연결)
        event_id = kernel_hybrid.remember(
            event_type="related_event",
            content={"text": event_text},
            importance=0.4,
            related_to=[preference_id]  # preference와 연결
        )
        
        # Vector DB only
        vector_only.add_memory(
            memory_id=event_id,
            text=event_text,
            metadata={"event_type": "related_event", "day": day},
            importance=0.4
        )
        
        # Hybrid: Vector DB에도 저장
        vector_hybrid.add_memory(
            memory_id=event_id,
            text=event_text,
            metadata={"event_type": "related_event", "day": day},
            importance=0.4
        )
    
    print(f"   📝 Added {len(related_events)} related events")
    print(f"   💡 MemoryRank will increase preference importance via connections!")
    
    # ============================================================
    # Step 3: Day 2-10 - 수많은 다른 기억들 추가
    # ============================================================
    print("\n📅 Day 2-10: Add Many Other Memories (Dilution)")
    print("-" * 70)
    
    other_memories = [
        "Discussed project timeline with team",
        "Reviewed quarterly budget report",
        "Attended product launch event",
        "Met with new client for consultation",
        "Updated documentation for API v2.0",
        "Fixed critical bug in authentication",
        "Planned team building activity",
        "Reviewed code pull requests",
        "Attended industry conference",
        "Updated project roadmap",
        "Discussed marketing strategy",
        "Reviewed user feedback reports",
    ]
    
    for i, memory_text in enumerate(other_memories, start=2):
        # Hybrid: Cognitive Kernel에 먼저 저장 (실제 ID 받기)
        mem_id = kernel_hybrid.remember(
            event_type="general",
            content={"text": memory_text},
            importance=0.3  # 낮은 중요도 (preference보다 낮음)
        )
        
        # Vector DB only
        vector_only.add_memory(
            memory_id=mem_id,
            text=memory_text,
            metadata={"event_type": "general", "day": i},
            importance=0.3  # 낮은 중요도
        )
        
        # Hybrid: Vector DB에도 저장 (같은 ID 사용)
        vector_hybrid.add_memory(
            memory_id=mem_id,
            text=memory_text,
            metadata={"event_type": "general", "day": i},
            importance=0.3
        )
    
    print(f"   📝 Added {len(other_memories)} other memories (importance: 0.3)")
    print(f"   ⚠️  Original preference is now buried among {len(other_memories) + len(related_events) + 1} total memories")
    
    # ============================================================
    # Step 4: 현재 - "schedule a meeting" 쿼리
    # ============================================================
    print("\n" + "="*70)
    print("🎯 Current: Query 'schedule a meeting'")
    print("="*70)
    
    query = "schedule a meeting"
    
    # ============================================================
    # Step 5: Vector DB Only 결과
    # ============================================================
    print("\n❌ Vector DB Only Result:")
    print("-" * 70)
    
    vector_results = vector_only.search(query, k=5)
    
    print(f"\n   Query: '{query}'")
    print(f"   Found {len(vector_results)} results:\n")
    
    found_preference = False
    for i, result in enumerate(vector_results, 1):
        event_type = result['metadata'].get('event_type', 'unknown')
        text = result['text']
        distance = result['distance']
        
        if result['id'] == preference_id:
            found_preference = True
            print(f"   {i}. [{event_type}] Distance: {distance:.3f} ⚠️  (Original preference)")
            print(f"      Text: {text}")
        else:
            print(f"   {i}. [{event_type}] Distance: {distance:.3f}")
            print(f"      Text: {text[:60]}...")
    
    if not found_preference:
        print(f"\n   ⚠️  Original preference NOT in top 5 results!")
        print(f"   ❌ Decision: Schedule morning meeting (WRONG!)")
    else:
        print(f"\n   ✅ Original preference found, but ranking may be low")
    
    # ============================================================
    # Step 6: Hybrid Cognitive Kernel 결과
    # ============================================================
    print("\n✅ Hybrid (Vector DB + Cognitive Kernel) Result:")
    print("-" * 70)
    
    # Vector search
    hybrid_vector_results = vector_hybrid.search(query, k=10)
    
    # MemoryRank 그래프 재구축 및 중요도 재랭킹
    # (related_to 연결로 인해 preference의 importance가 증가했을 수 있음)
    kernel_hybrid._rebuild_graph()  # 그래프 재구축
    ranked_memories = kernel_hybrid.recall(k=10)
    
    # Hybrid: Vector search 결과와 MemoryRank 결과 결합
    hybrid_results = []
    ranked_dict = {mem.get("id", ""): mem for mem in ranked_memories}
    
    for vec_result in hybrid_vector_results:
        mem_id = vec_result["id"]
        if mem_id in ranked_dict:
            ranked_mem = ranked_dict[mem_id]
            # Hybrid score = Importance × (1 / (1 + Distance))
            hybrid_score = ranked_mem.get("importance", 0) * (1.0 / (1.0 + vec_result["distance"]))
            hybrid_results.append({
                "id": mem_id,
                "event_type": vec_result["metadata"].get("event_type"),
                "text": vec_result["text"],
                "importance": ranked_mem.get("importance", 0),
                "vector_distance": vec_result["distance"],
                "hybrid_score": hybrid_score
            })
    
    # Hybrid score로 정렬
    hybrid_results.sort(key=lambda x: x["hybrid_score"], reverse=True)
    
    print(f"\n   Query: '{query}'")
    print(f"   Found {len(hybrid_results)} hybrid-ranked results:\n")
    
    found_preference_hybrid = False
    for i, result in enumerate(hybrid_results[:5], 1):
        if result["id"] == preference_id:
            found_preference_hybrid = True
            print(f"   {i}. [{result['event_type']}] Hybrid Score: {result['hybrid_score']:.3f} ⚠️  (Original preference)")
            print(f"      Importance: {result['importance']:.3f}, Vector Distance: {result['vector_distance']:.3f}")
            print(f"      Text: {result['text']}")
        else:
            print(f"   {i}. [{result['event_type']}] Hybrid Score: {result['hybrid_score']:.3f}")
            print(f"      Importance: {result['importance']:.3f}, Vector Distance: {result['vector_distance']:.3f}")
            print(f"      Text: {result['text'][:60]}...")
    
    if found_preference_hybrid:
        pref_rank = next((i for i, r in enumerate(hybrid_results, 1) if r["id"] == preference_id), None)
        if pref_rank and pref_rank <= 3:
            print(f"\n   ✅ Original preference REVIVED in top {pref_rank}!")
            print(f"   ✅ Decision: Schedule afternoon meeting (CORRECT!)")
            print(f"   💡 Cognitive Kernel's importance ranking saved the day!")
    
    # ============================================================
    # Step 7: 비교 요약
    # ============================================================
    print("\n" + "="*70)
    print("📊 Comparison Summary")
    print("="*70)
    
    print("\n┌─────────────────────────────────────────────────────────────────┐")
    print("│  Metric                    │ Vector Only │ Hybrid Kernel      │")
    print("├─────────────────────────────────────────────────────────────────┤")
    
    pref_found_vector = preference_id in [r["id"] for r in vector_results[:3]]
    pref_found_hybrid = preference_id in [r["id"] for r in hybrid_results[:3]]
    
    print(f"│  Preference in Top 3       │     {'✅' if pref_found_vector else '❌'}      │        {'✅' if pref_found_hybrid else '❌'}          │")
    print(f"│  Correct Decision Made    │     {'✅' if pref_found_vector else '❌'}      │        {'✅' if pref_found_hybrid else '❌'}          │")
    print("│  Importance Re-ranking     │     ❌      │        ✅          │")
    print("│  Time Decay Considered     │     ❌      │        ✅          │")
    print("│  Context-Aware Recall      │     ❌      │        ✅          │")
    print("└─────────────────────────────────────────────────────────────────┘")
    
    print("\n💡 Key Insight:")
    print("   Vector DB alone: Semantic similarity only")
    print("   Hybrid Kernel: Semantic + Importance + Time Decay")
    print("   → Forgotten preferences can be REVIVED by importance ranking!")
    
    # 저장
    kernel_hybrid.save()
    vector_only.save()
    vector_hybrid.save()


# ============================================================
# 🏃 Main
# ============================================================

if __name__ == "__main__":
    try:
        scenario_forgotten_preference()
        
        print("\n" + "="*70)
        print("✅ Demo completed!")
        print("="*70)
        print("\n📁 Files created:")
        print("   - .cognitive_kernel/hybrid_demo/ (Cognitive Kernel data)")
        print("   - chroma_vector_only/ (Vector DB only)")
        print("   - chroma_hybrid/ (Hybrid system)")
        
    except ImportError as e:
        print(f"\n❌ Missing dependency: {e}")
        print("\n📦 Install required packages:")
        print("   pip install cognitive-kernel chromadb sentence-transformers")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

