from celery import shared_task
from celery.contrib.abortable import AbortableTask
import time

@shared_task(bind=True, base=AbortableTask, ignore_result=False)
def add_numbers(self, a: int, b: int) -> int:
    total_steps = 30  # Total steps in the task
    for step in range(1, total_steps + 1):
        # Simulate work
        time.sleep(1)
        # Calculate percentage
        progress = (step / total_steps) * 100
        # Update task state with progress
        self.update_state(state="PROGRESS", meta={"progress": progress})
    
    # Final result
    return a + b
