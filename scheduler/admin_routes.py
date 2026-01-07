# scheduler/admin_routes.py
from fastapi import APIRouter
from scheduler.state import STOP_REQUESTS, pending_job

router = APIRouter()

@router.post("/admin/create_job")
async def create_job(job: dict):
    global pending_job
    pending_job = job
    return {"status": "queued"}

@router.post("/admin/stop_job/{job_id}")
async def stop_job(job_id: str):
    STOP_REQUESTS[job_id] = True
    return {"status": "stop_set", "job_id": job_id}
