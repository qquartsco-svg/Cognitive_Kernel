"""
🔗 Cognitive Kernel + LlamaIndex Integration Example

LlamaIndex의 ChatMemoryBuffer 인터페이스를 구현하여
Cognitive Kernel의 장기 기억을 LlamaIndex 에이전트에 통합합니다.

Features:
- Persistent memory across restarts
- PageRank-based importance ranking
- Automatic session management

Usage:
    pip install cognitive-kernel llama-index
    python examples/llamaindex_memory.py
"""

from typing import List, Dict, Any, Optional
from cognitive_kernel import CognitiveKernel

try:
    from llama_index.core.memory import BaseChatMemory, ChatMessage
    from llama_index.core.base.llms.types import ChatMessage, MessageRole
    LLAMAINDEX_AVAILABLE = True
except ImportError:
    LLAMAINDEX_AVAILABLE = False
    BaseChatMemory = None
    ChatMessage = None
    MessageRole = None


if LLAMAINDEX_AVAILABLE:
    class CognitiveKernelMemory(BaseChatMemory):
        """
        LlamaIndex-compatible memory using Cognitive Kernel.
        
        Provides:
        - Persistent storage (survives process restart)
        - PageRank-based importance ranking
        - Automatic decay over time
        """
        
        def __init__(self, session_name: str = "llamaindex_agent", **kwargs):
            super().__init__(**kwargs)
            self.kernel = CognitiveKernel(session_name)
            self.session_name = session_name
        
        def __enter__(self):
            self.kernel.__enter__()
            return self
        
        def __exit__(self, *args):
            self.kernel.__exit__(*args)
        
        def get_all(self) -> List[ChatMessage]:
            """Get all chat messages from memory."""
            memories = self.kernel.recall(k=50)  # Get recent memories
            
            messages = []
            for mem in memories:
                content = mem.get('content', {})
                if isinstance(content, dict):
                    text = content.get('text', str(content))
                else:
                    text = str(content)
                
                event_type = mem.get('event_type', 'message')
                
                # Determine role from event type
                if 'user' in event_type.lower() or 'human' in event_type.lower():
                    role = MessageRole.USER
                elif 'assistant' in event_type.lower() or 'ai' in event_type.lower():
                    role = MessageRole.ASSISTANT
                else:
                    role = MessageRole.USER  # Default
                
                messages.append(ChatMessage(
                    role=role,
                    content=text
                ))
            
            return messages
        
        def get(self, initial_token_count: Optional[int] = None) -> List[ChatMessage]:
            """Get chat messages, optionally limited by token count."""
            all_messages = self.get_all()
            
            if initial_token_count is None:
                return all_messages
            
            # Simple token estimation (rough: 1 token ≈ 4 chars)
            selected = []
            token_count = 0
            
            for msg in reversed(all_messages):  # Start from most recent
                msg_tokens = len(msg.content) // 4
                if token_count + msg_tokens <= initial_token_count:
                    selected.insert(0, msg)
                    token_count += msg_tokens
                else:
                    break
            
            return selected
        
        def put(self, message: ChatMessage) -> None:
            """Store a chat message in memory."""
            event_type = "user_message" if message.role == MessageRole.USER else "ai_response"
            
            self.kernel.remember(
                event_type=event_type,
                content={"text": message.content, "role": message.role.value},
                importance=0.7 if message.role == MessageRole.USER else 0.5
            )
        
        def set(self, messages: List[ChatMessage]) -> None:
            """Replace all messages in memory."""
            # Clear existing memories (create new session)
            self.kernel = CognitiveKernel(f"{self.session_name}_reset")
            
            # Add all messages
            for msg in messages:
                self.put(msg)
        
        def reset(self) -> None:
            """Clear all memories."""
            self.kernel = CognitiveKernel(f"{self.session_name}_reset")


# ============================================================
# 🎯 Demo: LlamaIndex Integration
# ============================================================

def demo_llamaindex_integration():
    """LlamaIndex + Cognitive Kernel 통합 데모"""
    
    if not LLAMAINDEX_AVAILABLE:
        print("\n❌ LlamaIndex not installed")
        print("\n📦 Install required packages:")
        print("   pip install llama-index")
        return
    
    print("\n" + "="*60)
    print("🔗 LlamaIndex + Cognitive Kernel Integration")
    print("="*60)
    
    # 1. Cognitive Kernel Memory 초기화
    print("\n📦 Step 1: Initialize Cognitive Kernel Memory")
    print("-" * 60)
    
    with CognitiveKernelMemory("llamaindex_demo") as memory:
        print("   ✅ Cognitive Kernel Memory initialized")
        
        # 2. 대화 저장
        print("\n💬 Step 2: Store Conversation")
        print("-" * 60)
        
        messages = [
            ChatMessage(role=MessageRole.USER, content="My name is Alice"),
            ChatMessage(role=MessageRole.ASSISTANT, content="Nice to meet you, Alice!"),
            ChatMessage(role=MessageRole.USER, content="I love hiking and photography"),
            ChatMessage(role=MessageRole.ASSISTANT, content="Those are great hobbies!"),
            ChatMessage(role=MessageRole.USER, content="Remember: I prefer afternoon meetings"),
            ChatMessage(role=MessageRole.ASSISTANT, content="Got it! I'll remember that."),
        ]
        
        for msg in messages:
            memory.put(msg)
            print(f"   ✅ Stored: [{msg.role.value}] {msg.content[:40]}...")
        
        print(f"\n   📝 Total messages stored: {len(messages)}")
    
    print("\n   💾 Session ended → Auto-saved to disk")
    
    # 3. 세션 복구 테스트
    print("\n🔄 Step 3: Session Recovery Test")
    print("-" * 60)
    
    with CognitiveKernelMemory("llamaindex_demo") as memory:
        recovered = memory.get_all()
        print(f"   ✅ Recovered {len(recovered)} messages from previous session")
        
        print("\n   Recovered messages:")
        for i, msg in enumerate(recovered[-3:], 1):  # Show last 3
            print(f"   {i}. [{msg.role.value}] {msg.content[:50]}...")
        
        # 4. 중요도 기반 회상
        print("\n📊 Step 4: Importance-Based Recall")
        print("-" * 60)
        
        # Cognitive Kernel의 recall 사용
        top_memories = memory.kernel.recall(k=3)
        print(f"\n   Top 3 memories by importance:")
        for i, mem in enumerate(top_memories, 1):
            content = mem.get('content', {})
            if isinstance(content, dict):
                text = content.get('text', str(content))
            else:
                text = str(content)
            print(f"   {i}. [{mem.get('event_type')}] Importance: {mem.get('importance', 0):.3f}")
            print(f"      Text: {text[:50]}...")
    
    print("\n" + "="*60)
    print("✅ Demo completed!")
    print("="*60)


# ============================================================
# 🚀 Full LlamaIndex Integration Example
# ============================================================

def full_llamaindex_example():
    """완전한 LlamaIndex 통합 예제 코드"""
    
    example_code = '''
# Full LlamaIndex Integration Code:

from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from examples.llamaindex_memory import CognitiveKernelMemory

# Initialize with persistent memory
with CognitiveKernelMemory("my_assistant") as memory:
    
    # Create LlamaIndex agent
    llm = OpenAI(model="gpt-4")
    
    # Use Cognitive Kernel as memory backend
    agent = ReActAgent.from_tools(
        tools=[],  # Add your tools here
        llm=llm,
        memory=memory,  # ← Persistent, ranked memory!
        verbose=True
    )
    
    # Chat with persistent memory
    response = agent.chat("Remember: I prefer morning meetings")
    print(response)
    
    # Next day (new process), agent still remembers!
    response = agent.chat("When should we schedule our call?")
    # Agent recalls: "You prefer morning meetings"
    
# Memory automatically saved!
'''
    print("\n" + "="*60)
    print("🔗 Full LlamaIndex Integration Example")
    print("="*60)
    print(example_code)


# ============================================================
# 🏃 Main
# ============================================================

if __name__ == "__main__":
    print("\n🧠 Cognitive Kernel + LlamaIndex Demo")
    print("━" * 60)
    
    try:
        demo_llamaindex_integration()
        full_llamaindex_example()
        
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
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

