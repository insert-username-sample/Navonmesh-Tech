import os
import json
import asyncio
from studio.core.tts_engine import QwenStudioTTS
from studio.core.video_engine import assemble_video, extract_9_16_snippet
from studio.core.gpu_locker import vram_manager

class AutoPipeline:
    def __init__(self):
        self.state_file = "studio/assets/storyboard_state.json"
        # We assume sample voices exist in studio/assets/voices/
        self.tts = QwenStudioTTS(
            voice_ref_path="studio/assets/voices/navonmesh_ref.wav",
            voice_txt_path="studio/assets/voices/navonmesh_ref.txt"
        )

    async def run_full_production(self, page=None):
        """
        Orchestrates the entire news-to-video pipeline.
        """
        if not os.path.exists(self.state_file):
            print("[PIPELINE] Error: No storyboard state found.")
            return

        with open(self.state_file, 'r') as f:
            data = json.load(f)
            blocks = data.get("blocks", [])

        if not blocks:
            print("[PIPELINE] Error: Storyboard is empty.")
            return

        # 1. TTS Generation for all blocks
        print("[PIPELINE] Phase 1: Generating Audio Assets...")
        all_scripts = []
        for block in blocks:
            # Combine EN + HI for a bilingual feel, or choose one
            script = f"{block['script_en']} ... {block['script_hi']}"
            audio_path = f"studio/temp/audio_{block['id']}.wav"
            
            # This is already @gpu_task deco'd, so it will wait for its turn
            self.tts.generate(script, audio_path)
            all_scripts.append(audio_path)

        # 2. Combine Audio
        # For the first version, we'll just concatenate them or process one-by-one.
        # Let's assume we want one master video.
        print("[PIPELINE] Phase 2: Assembling 4K Master Video...")
        # Placeholder: Using a folder of AI-generated tech images
        image_folder = "studio/assets/render_assets"
        os.makedirs(image_folder, exist_ok=True)
        
        # Ensure we have at least one image per block
        # (In a real scenario, we'd generate these per signal)
        
        # 3. Assemble
        master_output = f"daily_shorts/{blocks[0]['title'].replace(' ', '_')}_4K.mp4"
        os.makedirs("daily_shorts", exist_ok=True)
        
        # Using the first audio for now as a test, or we'd concatenate
        # For V1, we'll just process the first block as the primary reel
        final_video = assemble_video(all_scripts[0], image_folder, master_output)
        
        # 4. Extract Short (9:16)
        short_output = master_output.replace("_4K.mp4", "_SHORT_916.mp4")
        extract_9_16_snippet(final_video, short_output, start_time="00:00:00", duration="00:00:15")

        print(f"[PIPELINE] ✅ Production Complete: {final_video}")
        return final_video

if __name__ == "__main__":
    pipeline = AutoPipeline()
    asyncio.run(pipeline.run_full_production())
