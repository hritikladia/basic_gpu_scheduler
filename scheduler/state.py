# scheduler/state.py
from typing import Dict, Any, Optional
import time

# ---------- Job state ----------
JOB_STATUS: Dict[str, Dict[str, Any]] = {}
MAX_RETRIES = 1

JOBS: Dict[str, Dict[str, Any]] = {}  # job_id -> job object
JOB_QUEUE: list[str] = [] # FIFO list of job_ids


pending_job: Optional[Dict[str, Any]] = None

STOP_REQUESTS: Dict[str, bool] = {}
ASSIGNED_JOB_BY_AGENT: Dict[str, Dict[str, Any]] = {}

# ---------- Agent state ----------
AGENT_LAST_SEEN: Dict[str, int] = {}
AGENT_TIMEOUT = 15  # seconds

# ---------- Logs ----------
job_logs: Dict[str, list] = {}

def is_agent_stale(agent_id: str) -> bool:
    last = AGENT_LAST_SEEN.get(agent_id)
    if last is None:
        return False
    return (int(time.time()) - last) > AGENT_TIMEOUT
