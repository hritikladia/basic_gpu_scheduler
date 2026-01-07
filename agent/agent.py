# agent/agent.py
import time
import socket, uuid
from datetime import datetime

from gpu_utils import init_nvml
from state import STATE_IDLE
from job_manager import JobManager
from control_plane import build_sync_payload, sync_with_scheduler

SCHEDULER_BASE = "http://127.0.0.1:8000"

class Agent:
    def __init__(self, scheduler_base=SCHEDULER_BASE):
        self.agent_id = str(uuid.uuid4())
        self.hostname = socket.gethostname()
        self.scheduler_base = scheduler_base
        self.job_manager = JobManager(
            scheduler_base=scheduler_base,
            agent_id=self.agent_id
        )

    def run(self):
        print(f"Agent started. ID={self.agent_id}, Host={self.hostname}")

        if init_nvml():
            print("NVML initialized.")
        else:
            print("NVML NOT available.")

        self.job_manager.state = STATE_IDLE

        while True:
            now = datetime.now().strftime("%H:%M:%S")

            payload = build_sync_payload(self, self.job_manager)
            resp = sync_with_scheduler(self.scheduler_base, payload)

            print(f"[{now}] sync state={self.job_manager.state}")

            cmd = resp.get("command", "NOOP").upper()
            job = resp.get("job")

            if cmd == "RUN":
                self.job_manager.start_job(job)
            elif cmd == "KILL":
                expected = job.get("job_id") if isinstance(job, dict) else None
                self.job_manager.kill_job(expected)

            self.job_manager.poll_once()
            time.sleep(5)

if __name__ == "__main__":
    Agent().run()
