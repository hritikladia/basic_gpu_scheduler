# scheduler/log_routes.py
from fastapi import APIRouter
from scheduler.state import job_logs, JOB_STATUS, ASSIGNED_JOB_BY_AGENT, pending_job

router = APIRouter()

@router.post("/agent/log")
async def receive_log(payload: dict):
    job_id = payload["job_id"]
    job_logs.setdefault(job_id, []).append(payload["line"])
    return {"status": "ok"}

@router.get("/job/{job_id}/logs")
async def get_logs(job_id: str):
    return job_logs.get(job_id, [])

@router.get("/job/{job_id}/status")
async def get_status(job_id: str):
    if job_id in JOB_STATUS:
        return JOB_STATUS[job_id]

    for agent_id, job in ASSIGNED_JOB_BY_AGENT.items():
        if job.get("job_id") == job_id:
            return {"status": "RUNNING", "agent_id": agent_id}

    if pending_job and pending_job.get("job_id") == job_id:
        return {"status": "QUEUED"}

    return {"status": "UNKNOWN"}
