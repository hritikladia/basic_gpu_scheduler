from fastapi import APIRouter, HTTPException
from scheduler.state import JOBS, JOB_QUEUE, ASSIGNED_JOB_BY_AGENT

router = APIRouter()
@router.get("/jobs")
async def list_jobs():
    """
    Return a summary of all jobs known to the scheduler.
    """
    jobs = []

    for job_id, job in JOBS.items():
        jobs.append({
            "job_id": job_id,
            "status": job["status"],
            "assigned_agent": job["assigned_agent"],
            "submit_time": job["submit_time"],
            "start_time": job["start_time"],
            "end_time": job["end_time"],
        })

    return {
        "count": len(jobs),
        "jobs": jobs
    }

@router.get("/jobs/{job_id}")
async def get_job(job_id: str):
    """
    Return full details for a single job.
    """
    job = JOBS.get(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job
