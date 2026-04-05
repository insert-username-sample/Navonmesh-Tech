import asyncio
import json
import os
from studio.core.news_scout import NewsScout
from studio.core.brain_adapter import BrainAdapter

async def auto_init():
    print("[INIT] Starting Autonomous Initialization for Navonmesh Studio...")
    
    scout = NewsScout()
    brain = BrainAdapter()
    
    # 1. Scout trending signals
    signals = await scout.scout_signals()
    
    # 2. Draft storyboard blocks
    if not signals:
        print("[INIT] No signals found. Using fallback data.")
        signals = [{"source": "Manual", "items": ["DeepSeek-V4 Release", "NVIDIA Blackwell Benchmark", "Humanoid Robot S1"]}]
        
    blocks = brain.draft_storyboard(signals)
    
    # 3. Save to a persistent state file for the UI to load
    state_file = "studio/assets/storyboard_state.json"
    os.makedirs(os.path.dirname(state_file), exist_ok=True)
    
    with open(state_file, 'w') as f:
        json.dump({"blocks": blocks, "last_updated": str(asyncio.get_event_loop().time())}, f, indent=4)
        
    print(f"[INIT] ✅ Storyboard initialized with {len(blocks)} blocks.")
    print(f"[INIT] State saved to {state_file}")

if __name__ == "__main__":
    asyncio.run(auto_init())
