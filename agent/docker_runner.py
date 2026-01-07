# agent/docker_runner.py

import subprocess
import uuid
import select
import time

def start_docker_job(job):
    job_id = job["job_id"]
    image = job["image"]
    script = job["script"]
    gpus = job["gpus"]

    container_name = f"job_{job_id}_{uuid.uuid4().hex[:6]}"

    print(f"🐳 Starting Docker job {job_id} in container {container_name}")

    cmd = (
        f"docker run --name {container_name} "
        f"--gpus device={gpus} "
        f"-v /home/hritik/Desktop/scheduler/test:/workspace "
        f"{image} python3 /workspace/{script}"
    )

    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1   # line-buffered
    )

    return process, container_name


def drain_docker_logs_once(process, timeout_sec=0.2):
    """
    Non-blocking log drain.

    Reads whatever lines are currently available on stdout,
    waits up to timeout_sec, then returns.
    """
    lines = []

    if process.stdout is None:
        return lines

    # select() tells us if stdout has data ready to read
    ready, _, _ = select.select([process.stdout], [], [], timeout_sec)

    if ready:
        while True:
            line = process.stdout.readline()
            if not line:
                break
            lines.append(line.rstrip())

            # Stop if no more data is immediately available
            ready, _, _ = select.select([process.stdout], [], [], 0)
            if not ready:
                break

    return lines


def cleanup_container(container_name):
    print(f"🧹 Cleaning up container {container_name}")
    subprocess.run(f"docker rm -f {container_name}", shell=True)
