# agent/job_manager.py
import time
from state import STATE_IDLE, STATE_RUNNING, STATE_KILLING
from execution import (
    start_job_execution,
    drain_logs_once,
    cleanup_execution
)
from process_logging import push_log_line

class JobManager:
    def __init__(self, scheduler_base, agent_id):
        self.scheduler_base = scheduler_base
        self.agent_id = agent_id

        self.state = STATE_IDLE
        self.current_job_id = None
        self.current_container = None
        self.current_process = None
        self.started_at = None

        self.completed_job_result = None
        self.last_error = None

    def start_job(self, job):
        if self.state != STATE_IDLE:
            return

        try:
            process, container = start_job_execution(job)
        except Exception as e:
            self.last_error = f"start_failed: {repr(e)}"
            return

        self.state = STATE_RUNNING
        self.current_job_id = job["job_id"]
        self.current_container = container
        self.current_process = process
        self.started_at = int(time.time())
        self.last_error = None

        print(f"🚀 Job {self.current_job_id} started")

    def kill_job(self, expected_job_id=None):
        if self.state != STATE_RUNNING:
            return
        if expected_job_id and expected_job_id != self.current_job_id:
            return

        self.state = STATE_KILLING
        try:
            cleanup_execution(self.current_container)
        finally:
            self._clear_state()

    def poll_once(self):
        if self.state != STATE_RUNNING or not self.current_process:
            return

        try:
            for line in drain_logs_once(self.current_process):
                print(f"[Docker {self.current_job_id}] {line}")
                push_log_line(
                    self.scheduler_base,
                    self.agent_id,
                    self.current_job_id,
                    line
                )
        except Exception as e:
            self.last_error = f"log_drain_failed: {repr(e)}"

        exit_code = self.current_process.poll()
        if exit_code is not None:
            print(f"✔️ Job {self.current_job_id} finished ({exit_code})")
            try:
                cleanup_execution(self.current_container)
            except Exception:
                pass

            self.completed_job_result = {
                "job_id": self.current_job_id,
                "exit_code": exit_code,
                "ended_at": int(time.time())
            }

            self._clear_state()

    def _clear_state(self):
        self.current_job_id = None
        self.current_container = None
        self.current_process = None
        self.started_at = None
        self.state = STATE_IDLE
