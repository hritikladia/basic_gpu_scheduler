# scheduler/agent_routes.py
from fastapi import APIRouter
import time

from scheduler.state import AGENT_LAST_SEEN, ASSIGNED_JOB_BY_AGENT
from scheduler.scheduler_core import (
    handle_job_completion,
    should_kill_job,
    assign_job_to_agent,
)

router = APIRouter()

@router.post("/agent/sync")
async def agent_sync(payload: dict):
    agent_id = payload.get("agent_id")
    agent_state = payload.get("agent_state")
    current_job = payload.get("current_job")
    job_result = payload.get("job_result")

    AGENT_LAST_SEEN[agent_id] = int(time.time())

    # 1. Job completion
    if job_result:
        handle_job_completion(agent_id, job_result)

    # 2. Stop handling
    if agent_state == "RUNNING" and current_job:
        job_id = current_job.get("job_id")
        if should_kill_job(job_id):
            return {"command": "KILL", "job": {"job_id": job_id}}

        return {"command": "NOOP"}

    # 3. Assign new job
    if agent_state == "IDLE":
        job = assign_job_to_agent(agent_id)
        if job:
            return {
                "command": "RUN",
                "job": job,
                "reason": "fifo_queue_assignment"
            }


    return {"command": "NOOP"}
