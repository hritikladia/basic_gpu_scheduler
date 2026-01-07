# agent/execution.py
from docker_runner import start_docker_job, drain_docker_logs_once, cleanup_container

def start_job_execution(job):
    return start_docker_job(job)

def drain_logs_once(process):
    return drain_docker_logs_once(process)

def cleanup_execution(container_name):
    cleanup_container(container_name)



