import psutil
import platform

def gatherSystemInfo():
    print("System resource gathering listed below.\n")
    print(f"System: {platform.system()}")
    print(f"Node Name: {platform.node()}")
    print(f"Release: {platform.release()}")
    print(f"Version: {platform.version()}")
    print(f"Machine: {platform.machine()}")
    print(f"Processor: {platform.processor()}")
    print(f"CPU Usage: {psutil.cpu_percent(interval=1)}%")

gatherSystemInfo()