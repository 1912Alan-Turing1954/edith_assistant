import logging
import platform
import psutil
import time
import GPUtil
import socket

class SystemInfo:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    def get_system_info(self) -> dict:
        logging.info("Gathering system information.")
        system_info = {
            "Operating System": f"{platform.system()} {platform.release()}",
            "Computer Name": platform.node(),
            "CPU Info": self.get_cpu_info(),
            "Memory Info": self.get_memory_info(),
            "Disk Info": self.get_disk_info(),
            "Network Info": self.get_network_info(),
            "Uptime": self.get_uptime(),
            "Python Version": platform.python_version(),
        }
        if platform.system() == "Linux":
            system_info["Kernel Version"] = platform.uname().release
        system_info["Battery Status"] = self.get_battery_status()
        system_info["GPU Info"] = self.get_gpu_info()
        return system_info

    def get_cpu_info(self) -> dict:
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_count_physical = psutil.cpu_count(logical=False)
        cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
        return {
            "Physical Cores": cpu_count_physical,
            "Total Cores": cpu_count_logical,
            "CPU Usage": cpu_usage,
        }

    def get_memory_info(self) -> dict:
        memory = psutil.virtual_memory()
        return {
            "Total Memory": f"{memory.total / (1024 ** 3):.2f} GB",
            "Available Memory": f"{memory.available / (1024 ** 3):.2f} GB",
            "Used Memory": f"{memory.used / (1024 ** 3):.2f} GB",
            "Memory Usage": f"{memory.percent}%",
        }

    def get_disk_info(self) -> list:
        disk_info = []
        for partition in psutil.disk_partitions(all=False):
            partition_usage = psutil.disk_usage(partition.mountpoint)
            disk_info.append({
                "Drive": partition.device,
                "Mount Point": partition.mountpoint,
                "File System": partition.fstype,
                "Total Space": f"{partition_usage.total / (1024 ** 3):.2f} GB",
                "Used Space": f"{partition_usage.used / (1024 ** 3):.2f} GB",
                "Free Space": f"{partition_usage.free / (1024 ** 3):.2f} GB",
                "Disk Usage": f"{partition_usage.percent}%",
            })
        return disk_info

    def get_network_info(self) -> list:
        network_info = []
        for interface, addresses in psutil.net_if_addrs().items():
            for address in addresses:
                if address.family == socket.AF_INET:
                    network_info.append({
                        "Interface": interface,
                        "IP Address": address.address,
                        "Netmask": address.netmask,
                    })
                    break
        return network_info

    def get_uptime(self) -> str:
        uptime_seconds = time.time() - psutil.boot_time()
        return f"{uptime_seconds // 3600} hours {uptime_seconds % 3600 // 60} minutes"

    def get_battery_status(self) -> dict:
        battery = psutil.sensors_battery()
        if battery:
            return {
                "Percentage": f"{battery.percent}%",
                "Plugged In": battery.power_plugged,
                "Time Left": f"{battery.secsleft // 60} minutes" if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Charging"
            }
        return {}

    def get_gpu_info(self) -> list:
        try:
            gpus = GPUtil.getGPUs()
            return [{
                "GPU ID": gpu.id,
                "Name": gpu.name,
                "Load": f"{gpu.load * 100}%",
                "Memory Total": f"{gpu.memoryTotal} MB",
                "Memory Free": f"{gpu.memoryFree} MB",
                "Memory Used": f"{gpu.memoryUsed} MB",
            } for gpu in gpus]
        except Exception as e:
            logging.error(f"Unable to retrieve GPU info: {str(e)}")
            return "Unable to retrieve GPU info."

