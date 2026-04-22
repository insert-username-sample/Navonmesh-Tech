import os
import sys
from huggingface_hub import snapshot_download

os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

target_root = r"F:\Projects\TernaryBonsai\models"
# Exact repo names from search
models = [
    "prism-ml/Ternary-Bonsai-8B-unpacked",
    "prism-ml/Ternary-Bonsai-4B-unpacked"
]

def download_models():
    if not os.path.exists(target_root):
        os.makedirs(target_root)
    
    for repo_id in models:
        model_name = repo_id.split("/")[-1]
        local_dir = os.path.join(target_root, model_name)
        print(f"[*] Downloading {repo_id} to {local_dir}...")
        try:
            snapshot_download(
                repo_id=repo_id,
                local_dir=local_dir,
                local_dir_use_symlinks=False,
                resume_download=True
            )
            print(f"[+] Downloaded {model_name} successfully.")
        except Exception as e:
            print(f"[!] Error downloading {repo_id}: {e}")

if __name__ == "__main__":
    download_models()
