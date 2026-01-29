"""
🧠 Cognitive Kernel + LangChain Integration Example

This example shows how to give your LangChain agent persistent, ranked long-term memory.

## Before (Standard LangChain):
- Memory resets on restart
- No importance ranking
- Simple FIFO buffer

## After (With Cognitive Kernel):
- Memory persists across restarts ✅
- PageRank-based importance recall ✅
- Automatic session management ✅

Usage:
    pip install cognitive-kernel langchain langchain-openai
    python langchain_memory.py
"""

from typing import Any, Dict, List, Optional
from cognitive_kernel import CognitiveKernel

# ============================================================
# 🧠 CognitiveKernelMemory - LangChain Compatible Memory Class
# ============================================================

class CognitiveKernelMemory:
    """
    LangChain-compatible memory using Cognitive Kernel.
    
    Provides:
    - Persistent storage (survives process restart)
    - PageRank-based importance ranking
    - Automatic decay over time
    """
    
    def __init__(self, session_name: str = "langchain_agent"):
        self.kernel = CognitiveKernel(session_name)
        self.memory_key = "history"
    
    def __enter__(self):
        self.kernel.__enter__()
        return self
    
    def __exit__(self, *args):
        self.kernel.__exit__(*args)
    
    @property
    def memory_variables(self) -> List[str]:
        return [self.memory_key]
    
    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        """Load relevant memories based on importance ranking."""
        memories = self.kernel.recall(k=5)
        
        if not memories:
            return {self.memory_key: ""}
        
        # Format memories for LLM context
        formatted = []
        for mem in memories:
            event_type = mem.get('event_type', 'memory')
            content = mem.get('content', {})
            importance = mem.get('importance', 0)
            
            if isinstance(content, dict):
                text = content.get('text', str(content))
            else:
                text = str(content)
            
            formatted.append(f"[{event_type}] (importance: {importance:.2f}) {text}")
        
        return {self.memory_key: "\n".join(formatted)}
    
    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """Save conversation turn to long-term memory."""
        # Save user input
        if "input" in inputs:
            self.kernel.remember(
                event_type="user_message",
                content={"text": inputs["input"], "role": "user"},
                importance=0.7
            )
        
        # Save AI output
        if "output" in outputs:
            self.kernel.remember(
                event_type="ai_response",
                content={"text": outputs["output"], "role": "assistant"},
                importance=0.5
            )
    
    def clear(self) -> None:
        """Clear all memories (use with caution)."""
        # Note: This creates a new session, old data is preserved in files
        self.kernel = CognitiveKernel(f"{self.kernel.session_name}_cleared")


# ============================================================
# 🎯 Demo: Before vs After Comparison
# ============================================================

def demo_without_cognitive_kernel():
    """Standard approach: Memory lost on restart."""
    print("\n" + "="*60)
    print("❌ WITHOUT Cognitive Kernel (Standard Memory)")
    print("="*60)
    
    # Simulated conversation memory (in-memory only)
    memory = []
    
    # Session 1: User talks to agent
    memory.append({"role": "user", "text": "My name is Alice"})
    memory.append({"role": "assistant", "text": "Nice to meet you, Alice!"})
    memory.append({"role": "user", "text": "I love hiking and photography"})
    memory.append({"role": "assistant", "text": "Those are great hobbies!"})
    
    print(f"\n📝 Session 1: Stored {len(memory)} messages")
    print(f"   Memory contents: {[m['text'][:30] for m in memory]}")
    
    # Session 2: Simulate restart (memory lost!)
    memory = []  # Memory cleared on "restart"
    
    print(f"\n🔄 Session 2: After 'restart'")
    print(f"   Memory contents: {memory}")
    print(f"   ⚠️  Agent forgot everything!")
    
    return memory


def demo_with_cognitive_kernel():
    """With Cognitive Kernel: Memory persists and ranks by importance."""
    print("\n" + "="*60)
    print("✅ WITH Cognitive Kernel (Persistent Memory)")
    print("="*60)
    
    # Session 1: User talks to agent
    with CognitiveKernelMemory("demo_agent") as memory:
        # Simulate conversation
        memory.save_context(
            {"input": "My name is Alice"},
            {"output": "Nice to meet you, Alice!"}
        )
        memory.save_context(
            {"input": "I love hiking and photography"},
            {"output": "Those are great hobbies!"}
        )
        memory.save_context(
            {"input": "Tomorrow I have an important job interview"},
            {"output": "Good luck with your interview!"}
        )
        
        recalled = memory.load_memory_variables({})
        print(f"\n📝 Session 1: Stored 3 conversation turns")
        print(f"   Recalled memories:\n{recalled[memory.memory_key]}")
    # Auto-saved on exit!
    
    print("\n   💾 Session ended → Auto-saved to disk")
    
    # Session 2: Simulate restart (memory persists!)
    print(f"\n🔄 Session 2: After 'restart' (new process)")
    
    with CognitiveKernelMemory("demo_agent") as memory:
        recalled = memory.load_memory_variables({})
        print(f"   Recalled memories:\n{recalled[memory.memory_key]}")
        print(f"\n   ✅ Agent remembers everything!")
        print(f"   ✅ Memories ranked by importance (PageRank)")
    
    return recalled


# ============================================================
# 🚀 LangChain Integration Example (Full)
# ============================================================

def langchain_integration_example():
    """
    Full LangChain integration example.
    
    Requires: pip install langchain langchain-openai
    """
    print("\n" + "="*60)
    print("🔗 LangChain Integration Example")
    print("="*60)
    
    example_code = '''
# Full LangChain Integration Code:

from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from examples.langchain_memory import CognitiveKernelMemory

# Initialize with persistent memory
with CognitiveKernelMemory("my_assistant") as memory:
    
    # Create LangChain conversation
    llm = ChatOpenAI(model="gpt-4")
    
    # Use Cognitive Kernel as memory backend
    conversation = ConversationChain(
        llm=llm,
        memory=memory,  # ← Persistent, ranked memory!
        verbose=True
    )
    
    # Chat with persistent memory
    response = conversation.predict(input="Remember: I prefer morning meetings")
    print(response)
    
    # Next day (new process), agent still remembers!
    response = conversation.predict(input="When should we schedule our call?")
    # Agent recalls: "You prefer morning meetings"
    
# Memory automatically saved!
'''
    print(example_code)


# ============================================================
# 🏃 Main
# ============================================================

if __name__ == "__main__":
    print("\n🧠 Cognitive Kernel + LangChain Demo")
    print("━" * 60)
    
    # Show the difference
    demo_without_cognitive_kernel()
    demo_with_cognitive_kernel()
    
    # Show integration code
    langchain_integration_example()
    
    print("\n" + "="*60)
    print("📊 Summary")
    print("="*60)
    print("""
┌─────────────────────────────────────────────────────────┐
│  Feature              │ Standard │ Cognitive Kernel     │
├─────────────────────────────────────────────────────────┤
│  Persistence          │    ❌    │       ✅            │
│  Importance Ranking   │    ❌    │       ✅ (PageRank) │
│  Time Decay           │    ❌    │       ✅            │
│  Session Management   │  Manual  │       Automatic     │
│  Storage Backend      │  Memory  │  JSON/SQLite/NPZ    │
└─────────────────────────────────────────────────────────┘
    """)
    
    print("\n🚀 Get started:")
    print("   pip install cognitive-kernel")
    print("   python examples/langchain_memory.py")

