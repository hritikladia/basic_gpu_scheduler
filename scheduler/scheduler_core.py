# scheduler/scheduler_core.py
import time
import uuid
from datetime import datetime
from scheduler.state import JOBS, JOB_QUEUE

from scheduler.state import (
    JOB_STATUS,
    MAX_RETRIES,
    STOP_REQUESTS,
    ASSIGNED_JOB_BY_AGENT,
    pending_job,
    JOBS,
    JOB_QUEUE
)

def handle_job_completion(agent_id, job_result):
    global pending_job

    job_id = job_result["job_id"]
    exit_code = job_result["exit_code"]
    ended_at = job_result["ended_at"]

    status = "SUCCEEDED" if exit_code == 0 else "FAILED"

    JOB_STATUS[job_id] = {
        "status": status,
        "exit_code": exit_code,
        "ended_at": ended_at,
        "retries": JOB_STATUS.get(job_id, {}).get("retries", 0),
    }

    assigned_job = ASSIGNED_JOB_BY_AGENT.pop(agent_id, None)

    if status == "FAILED" and assigned_job:
        retries = JOB_STATUS[job_id]["retries"]
        if retries < MAX_RETRIES:
            JOB_STATUS[job_id]["retries"] += 1
            pending_job = assigned_job

    return status


def should_kill_job(job_id: str) -> bool:
    return STOP_REQUESTS.get(job_id, False)


def assign_job_to_agent(agent_id: str):
    """
    Assign the next queued job to the given agent (FIFO).
    Returns the job dict, or None if no job is available.
    """

    # 1. If no jobs are waiting, nothing to do
    if not JOB_QUEUE:
        return None

    # 2. Pop the oldest job (FIFO)
    job_id = JOB_QUEUE.pop(0)
    job = JOBS[job_id]

    # 3. Update job state
    job["status"] = "RUNNING"
    job["assigned_agent"] = agent_id
    job["start_time"] = datetime.now()

    # 4. Track assignment
    ASSIGNED_JOB_BY_AGENT[agent_id] = job

    return job


def create_job(job_data: dict) -> dict:
    job_id = str(uuid.uuid4())

    job = {
        "job_id": job_id,
        "user": job_data.get("user", "unknown"),
        "image": job_data["image"],
        "script": job_data["script"],
        "gpus": job_data["gpus"],
        "status": "QUEUED",
        "assigned_agent": None,
        "submit_time": datetime.now(),
        "start_time": None,
        "end_time": None,
    }

    JOBS[job_id] = job
    JOB_QUEUE.append(job_id)

    return job
