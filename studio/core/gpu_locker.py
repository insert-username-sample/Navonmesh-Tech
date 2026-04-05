import threading
import time
from enum import Enum, auto

class GpuPriority(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()

class GpuLocker:
    """
    A centralized semaphore to manage access to the RTX 3060 Ti's 8GB VRAM.
    Ensures that only one memory-intensive task (LLM, TTS, or Render) is active.
    """
    _instance = None
    _lock = threading.Lock()
    _gpu_semaphore = threading.Semaphore(1)

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(GpuLocker, cls).__new__(cls)
                cls._instance.active_task = None
                cls._instance.task_start_time = None
        return cls._instance

    def acquire(self, task_name: str, priority: GpuPriority = GpuPriority.MEDIUM):
        print(f"[VRAM] Task '{task_name}' (Priority: {priority.name}) is waiting for GPU access...")
        self._gpu_semaphore.acquire()
        self.active_task = task_name
        self.task_start_time = time.time()
        print(f"[VRAM] >>> GPU LOCKED by '{task_name}'")

    def release(self):
        duration = time.time() - self.task_start_time if self.task_start_time else 0
        print(f"[VRAM] <<< GPU RELEASED by '{self.active_task}' (Duration: {duration:.2f}s)")
        self.active_task = None
        self.task_start_time = None
        self._gpu_semaphore.release()

    def get_status(self):
        return {
            "is_locked": self.active_task is not None,
            "active_task": self.active_task,
            "elapsed": time.time() - self.task_start_time if self.task_start_time else 0
        }

# Global Instance
vram_manager = GpuLocker()

def gpu_task(task_name: str, priority: GpuPriority = GpuPriority.MEDIUM):
    """
    Decorator for functions that require GPU access.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            vram_manager.acquire(task_name, priority)
            try:
                return func(*args, **kwargs)
            finally:
                vram_manager.release()
        return wrapper
    return decorator
