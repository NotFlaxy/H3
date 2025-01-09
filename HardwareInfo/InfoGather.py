import psutil
import platform
from datetime import datetime

def gatherSystemInfo():
    print("System resource log listed below.\n")
    
    # Gather date and time for logging.
    currentTime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    print("Time of logging: " + currentTime + "\n")

    print("Software Resources:")
    print(f"System: {platform.system()}")
    print(f"Release: {platform.release()}")
    print(f"Node Name: {platform.node()}")
    print(f"Version: {platform.version()}")

    print("\nHardware Resources:")
    print(f"Machine: {platform.machine()}")
    print(f"Processor: {platform.processor()}")
    
    # CPU Usage
    print(f"CPU Usage: {psutil.cpu_percent(interval=1)}%")
    
    # Memory Usage
    memory = psutil.virtual_memory()
    print(f"Total Memory: {memory.total / (1024 ** 3):.2f} GB")
    print(f"Used Memory: {memory.used / (1024 ** 3):.2f} GB")
    print(f"Memory Usage: {memory.percent}%")

    # Disk Usage
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"Disk: {partition.device}, Usage: {usage.percent}%")
        except Exception as e:
            print(f"Could not access disk {partition.device}: {e}")

    # Network I/O
    net_io = psutil.net_io_counters()
    print("\nNetwork Resources:")
    print(f"Bytes Sent: {net_io.bytes_sent / (1024 ** 2):.2f} MB")
    print(f"Bytes Received: {net_io.bytes_recv / (1024 ** 2):.2f} MB")

    print("\nEnd of system resource log.")

gatherSystemInfo()