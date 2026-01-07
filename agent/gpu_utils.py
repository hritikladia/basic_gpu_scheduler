# # agent/gpu_utils.py
import pynvml

def init_nvml():
    try:
        pynvml.nvmlInit()
        return True
    except Exception:
        return False


def get_real_gpus():
    gpu_list = []

    try:
        count = pynvml.nvmlDeviceGetCount()
    except:
        return []  # no GPUs or NVML init failure

    for i in range(count):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)

        mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
        util = pynvml.nvmlDeviceGetUtilizationRates(handle)
        temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
        name = pynvml.nvmlDeviceGetName(handle).decode()

        gpu_list.append({
            "id": i,
            "name": name,
            "memory_total": mem.total,
            "memory_used": mem.used,
            "utilization": util.gpu,
            "temperature": temp,
        })

    return gpu_list
