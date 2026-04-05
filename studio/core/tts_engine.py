import os
import re
import torch
import numpy as np
import soundfile as sf
from qwen_tts import Qwen3TTSModel
from studio.core.gpu_locker import gpu_task, GpuPriority

class QwenStudioTTS:
    def __init__(self, voice_ref_path, voice_txt_path):
        self.voice_ref = voice_ref_path
        self.voice_txt = voice_txt_path
        self.model = None
        self.ref_text = self._load_ref_text()

    def _load_ref_text(self):
        try:
            with open(self.voice_txt, 'r', encoding='utf-8') as f:
                return f.read().strip().replace('\n', ' ')
        except Exception as e:
            print(f"[TTS] Warning: Could not read reference text: {e}")
            return ""

    def clean_script(self, text):
        """Strips out stage directions, actions, and labels."""
        text = re.sub(r'\[.*?\]', '', text)
        text = re.sub(r'\*.*?\*', '', text)
        text = re.sub(r'(?i)Scene \d+:?', '', text)
        text = re.sub(r'(?m)^[A-Z\s]+:\s*', '', text)
        return text.replace('**', '').replace('__', '').strip()

    def split_text(self, text, max_len=200):
        text = re.sub(r'\n+', ' ', text)
        parts = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        curr = ""
        for p in parts:
            if len(curr) + len(p) <= max_len:
                curr += p + " "
            else:
                if curr.strip(): chunks.append(curr.strip())
                curr = p + " "
        if curr.strip(): chunks.append(curr.strip())
        return chunks

    @gpu_task("Qwen-TTS Synthesis", priority=GpuPriority.HIGH)
    def generate(self, text, output_path):
        if self.model is None:
            print("[TTS] Loading 1.7B Qwen3 Model into VRAM...")
            device = "cuda:0" if torch.cuda.is_available() else "cpu"
            dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
            
            self.model = Qwen3TTSModel.from_pretrained(
                "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
                device_map=device,
                dtype=dtype,
                attn_implementation="flash_attention_2" if device == "cuda:0" else "eager",
            )

        clean_text = self.clean_script(text)
        chunks = self.split_text(clean_text)
        print(f"[TTS] Generating {len(chunks)} chunks...")

        all_wavs = []
        sample_rate = 24000
        
        for i, chunk in enumerate(chunks):
            if not chunk.strip(): continue
            wavs, sr = self.model.generate_voice_clone(
                text=chunk,
                language="Auto",
                ref_audio=self.voice_ref,
                ref_text=self.ref_text,
            )
            sample_rate = sr
            audio_data = wavs[0]
            if hasattr(audio_data, 'cpu'):
                audio_data = audio_data.cpu().numpy()
            all_wavs.append(audio_data.flatten())
            
        if all_wavs:
            final_audio = np.concatenate(all_wavs, axis=0)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            sf.write(output_path, final_audio, sample_rate)
            print(f"[TTS] ✅ Saved: {output_path}")
            return output_path
        return None
