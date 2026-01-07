# agent/control_plane.py
import time
import requests
from gpu_utils import get_real_gpus

def build_sync_payload(agent, job_manager):
    payload = {
        "agent_id": agent.agent_id,
        "hostname": agent.hostname,
        "timestamp": int(time.time()),
        "agent_state": job_manager.state,
        "gpu_stats": {"gpus": get_real_gpus()},
        "current_job": None,
        "last_error": job_manager.last_error,
        "job_result": job_manager.completed_job_result,
    }

    if job_manager.state in ("RUNNING", "KILLING") and job_manager.current_job_id:
        payload["current_job"] = {
            "job_id": job_manager.current_job_id,
            "started_at": job_manager.started_at,
        }

    return payload


def sync_with_scheduler(scheduler_base, payload):
    try:
        resp = requests.post(
            f"{scheduler_base}/agent/sync",
            json=payload,
            timeout=5
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"command": "NOOP", "reason": f"sync_failed: {repr(e)}"}