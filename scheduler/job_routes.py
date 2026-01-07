# scheduler/job_routes.py
from fastapi import APIRouter, HTTPException
from scheduler.scheduler_core import create_job

router = APIRouter()

@router.post("/jobs/submit")
async def submit_job(job_data: dict):
    required_fields = ["image", "script", "gpus"]
    for field in required_fields:
        if field not in job_data:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required field: {field}"
            )

    job = create_job(job_data)

    return {
        "message": "Job submitted",
        "job_id": job["job_id"],
        "status": job["status"],
    }
