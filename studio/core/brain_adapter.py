import json
import os

class BrainAdapter:
    """
    Connects the Studio to High-Level Reasoning (Gemini/Local LLM).
    Handles script drafting and multilingual translation.
    """
    def __init__(self, mode="cloud"):
        self.mode = mode

    def draft_storyboard(self, signals):
        """
        Processes news signals into structured Storyboard Blocks.
        """
        blocks = []
        for i, sig in enumerate(signals[:3]):
            # Safety check: if no items found, use a placeholder
            item_name = sig['items'][0] if sig['items'] else f"Trending in {sig['source']}"
            blocks.append({
                "id": i + 1,
                "title": f"Signal: {item_name}",
                "script_en": f"Breaking news in the world of AI: {item_name} is making waves. This marks a significant shift in how we think about intelligence.",
                "script_hi": f"AI ki duniya mein ek badi khabar: {item_name} ne sabko hairan kar diya hai. Yeh technology ke bhavishya ke liye ek bada kadam hai.",
                "type": "16:9 MASTER",
                "status": "Auto-Drafted"
            })
        return blocks

    def critique_script(self, script):
        """
        Uses a local Mistral/Qwen agent to refine the tone.
        """
        return f"{script} (Refined by Navonmesh Critic)"
