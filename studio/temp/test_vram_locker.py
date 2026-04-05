import threading
import time
import random
from studio.core.gpu_locker import gpu_task, GpuPriority

@gpu_task("Heavy Model Task", priority=GpuPriority.HIGH)
def simulated_heavy_task(name):
    print(f"Task '{name}' started (Heavy Load)...")
    time.sleep(random.uniform(5, 7))
    print(f"Task '{name}' finished.")

@gpu_task("Quick Inference Task", priority=GpuPriority.LOW)
def simulated_quick_task(name):
    print(f"Task '{name}' started (Quick Load)...")
    time.sleep(random.uniform(1, 2))
    print(f"Task '{name}' finished.")

def run_test():
    print("--- Starting VRAM Concurrency Test ---")
    threads = [
        threading.Thread(target=simulated_heavy_task, args=("Model_Trainer_1",)),
        threading.Thread(target=simulated_quick_task, args=("TTS_Inference_1",)),
        threading.Thread(target=simulated_heavy_task, args=("Video_Renderer_1",)),
    ]
    
    for t in threads:
        t.start()
        time.sleep(1) # Stagger starts

    for t in threads:
        t.join()
    print("--- VRAM Concurrency Test Finished ---")

if __name__ == "__main__":
    run_test()
