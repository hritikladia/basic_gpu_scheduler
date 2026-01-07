# agent/logging.py
import requests

def push_log_line(scheduler_base, agent_id, job_id, line):
    """Best-effort log push. Must never crash job execution."""
    try:
        requests.post(
            f"{scheduler_base}/agent/log",
            json={
                "agent_id": agent_id,
                "job_id": job_id,
                "line": line
            },
            timeout=2
        )
    except:
        pass
