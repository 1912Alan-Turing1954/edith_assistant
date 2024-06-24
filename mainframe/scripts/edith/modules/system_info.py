import psutil
import platform
import socket
import time
import random


def get_system_info():
    system_info = {}

    # Operating System
    system_info["Operating System"] = f"{platform.system()} {platform.release()}"

    # Computer Name
    system_info["Computer Name"] = psutil.users()[0].name

    # CPU Information
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    system_info["CPU Info"] = {
        "Physical Cores": psutil.cpu_count(logical=False),
        "Total Cores": psutil.cpu_count(logical=True),
        "CPU Usage": cpu_usage,
    }

    # Memory Information
    memory = psutil.virtual_memory()
    system_info["Total Memory"] = f"{round(memory.total / (1024 ** 3), 2)} GB"
    system_info["Available Memory"] = f"{round(memory.available / (1024 ** 3), 2)} GB"
    system_info["Used Memory"] = f"{round(memory.used / (1024 ** 3), 2)} GB"
    system_info["Memory Usage"] = f"{memory.percent}%"

    # Disk Information
    partitions = psutil.disk_partitions(all=False)
    system_info["Disk Info"] = []
    for partition in partitions:
        partition_usage = psutil.disk_usage(partition.mountpoint)
        system_info["Disk Info"].append(
            {
                "Drive": partition.device,
                "Mount Point": partition.mountpoint,
                "File System": partition.fstype,
                "Total Space": f"{round(partition_usage.total / (1024 ** 3), 2)} GB",
                "Used Space": f"{round(partition_usage.used / (1024 ** 3), 2)} GB",
                "Free Space": f"{round(partition_usage.free / (1024 ** 3), 2)} GB",
                "Disk Usage": f"{partition_usage.percent}%",
            }
        )

    # Network Information
    network_info = psutil.net_if_addrs()
    system_info["Network Info"] = []
    for interface, addresses in network_info.items():
        for address in addresses:
            if address.family == socket.AF_INET:
                system_info["Network Info"].append(
                    {
                        "Interface": interface,
                        "IP Address": address.address,
                        "Netmask": address.netmask,
                    }
                )
                break

    return system_info


system_status_phrases = [
    "I have extracted your machine details.",
    "Here are your system specifications.",
    "Your machine's information has been retrieved.",
    "Your PC's current status has been analyzed.",
    "I've collected the necessary data about your system.",
]

cpu_usage_phrases = [
    "Your C P U usage is currently at {cpu_usage}%",
    "C P U utilization stands at {cpu_usage}%",
    "The C P U load is around {cpu_usage}%",
    "Currently, your C P U is operating at {cpu_usage}%",
]

memory_usage_phrases = [
    "Your memory usage is currently at {memory_usage}%",
    "Memory utilization stands at {memory_usage}%",
    "Your RAM is currently used up to {memory_usage}%",
    "Currently, your memory usage is {memory_usage}%",
]

storage_status_phrases = [
    "I have obtained your storage details.",
    "Here is your storage information.",
    "Your storage status has been retrieved.",
    "I've gathered information about your storage.",
]


# Define lists of phrases for different response types
positive_phrases = [
    "Your system is operating within normal parameters.",
    "No issues detected with your system performance.",
    "Everything appears to be functioning properly.",
]

concerned_phrases = [
    "I've identified a few concerns with your system's performance.",
    "Your system requires attention to optimize performance.",
    "There are issues that need addressing in your system.",
]

witty_phrases = {
    "cpu": [
        "Your CPU usage is quite high at the moment.",
        "CPU resources are under heavy load.",
        "Monitoring shows high CPU activity.",
    ],
    "memory": [
        "Memory usage is approaching critical levels.",
        "Your system is running low on available memory.",
        "Memory resources are being heavily utilized.",
    ],
    "disk": [
        "Disk space is nearing capacity and may impact performance.",
        "The available disk space is running low.",
        "Disk usage is high, consider freeing up space.",
    ],
    "network": [
        "The network connection is unstable.",
        "There are issues with the network connectivity.",
        "Network performance is currently degraded logan.",
    ],
    "positive_network": [
        "Your network is functioning perfectly.",
        "The network is stable and operational.",
        "No issues detected with your network.",
        "Everything seems fine with your network.",
        "Your network is up and running smoothly.",
    ],
    "battery": [
        "Battery is running low. Please connect the charger.",
        "Your device battery is critically low.",
        "Battery level is below optimal. Charging is recommended.",
    ],
}

import socket


def check_internet(host="8.8.8.8", port=53, timeout=2):
    """
    Check internet connectivity by trying to create a socket connection to a specified host and port.
    Default is Google's public DNS server (8.8.8.8).
    """
    network = None

    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        network = True
    except socket.error:
        network = False

    if network:
        repsonse = random.choice(witty_phrases["positive_network"])
        return repsonse
    if network == False:
        repsonse = random.choice(witty_phrases["network"])
        return repsonse


# def generate_system_status_response(system_info):
#     response_type = random.choice(["positive", "concerned"])

#     if response_type == "positive":
#         response = random.choice(positive_phrases)
#     else:
#         response = random.choice(concerned_phrases)

#     cpu_usage = max(system_info["CPU Info"]["CPU Usage"])
#     memory_usage = float(system_info["Memory Usage"][:-1])

#     if cpu_usage > 80:
#         response += " " + random.choice(witty_phrases["cpu"])

#     if memory_usage > 65:
#         response += " " + random.choice(witty_phrases["memory"])

#     # Check disk usage from 'Disk Info'
#     for disk in system_info["Disk Info"]:
#         disk_usage = float(disk["Disk Usage"][:-1])
#         if disk_usage > 90:
#             response += " " + random.choice(witty_phrases["disk"])
#             break  # Stop after the first occurrence

#     network_status = system_info.get("Network Status", "")
#     if network_status == "Disconnected":
#         response += " " + random.choice(witty_phrases["network"])

#     # Check if 'Battery Status' exists
#     battery_status = system_info.get("Battery Status", "")
#     if battery_status == "Low":
#         battery_response = random.choice(witty_phrases["battery"])
#         if random.random() < 0.3:  # Adjust the probability as needed
#             battery_response += " Sir."
#         response += " " + battery_response

#     return response


def generate_storage_status_response(system_info):
    response = random.choice(storage_status_phrases)
    free_disk_space = system_info["Disk Info"][0]["Free Space"]
    free_disk_space = free_disk_space.replace("GB", "gigabytes")
    disk_usage = float(system_info["Disk Info"][0]["Disk Usage"][:-1])
    overall_wellbeing = "healthy"

    if disk_usage > 75:
        overall_wellbeing = "concerned"
        response += " I must express my concern as your PC's storage is currently under considerable strain."
        response += " To ensure optimal performance, it is highly advisable to uninstall any unnecessary programs or games that are taking up excessive space."

    if disk_usage < 50:
        overall_wellbeing = "healthy"
        response += " Your PC's storage exhibits an exemplary state of operation."

    if overall_wellbeing == "healthy":
        response += f" At the moment, your PC has {free_disk_space} of free space, and your storage usage is at {str(disk_usage)}%."
    else:
        response += f" I am a tad concerned about your PC's storage health. Your storage usage is at {str(disk_usage)}. It would be prudent to follow the aforementioned recommendations to enhance its overall storage performance."

    return response


def generate_cpu_usage_response(info_system):
    cpu_usage = max(info_system["CPU Info"]["CPU Usage"])
    cpu_usage = round(cpu_usage, 2)
    response = random.choice(cpu_usage_phrases).format(cpu_usage=cpu_usage)
    return response


def generate_memory_usage_response(info_system):
    memory_usage = float(info_system["Memory Usage"][:-1])
    memory_usage = round(memory_usage, 2)
    response = random.choice(memory_usage_phrases).format(memory_usage=memory_usage)
    return response


def generate_disk_space_response(info_system):
    free_disk_space = info_system["Disk Info"][0]["Free Space"]
    free_disk_space = free_disk_space.replace("GB", "gigabytes")
    disk_usage = float(info_system["Disk Info"][0]["Disk Usage"][:-1])
    disk_usage = round(disk_usage, 2)
    response = random.choice(storage_status_phrases).format(
        free_disk_space=free_disk_space, disk_usage=disk_usage
    )
    return response


def generate_system_status_response(system_info):
    if not isinstance(system_info, dict):
        raise ValueError("Expected 'system_info' to be a dictionary.")

    response_type = random.choice(["positive", "concerned"])
    response = ""

    if response_type == "positive":
        response = random.choice(positive_phrases)
    else:
        response = random.choice(concerned_phrases)

    # Ensure 'CPU Info' is correctly accessed
    if "CPU Info" in system_info:
        cpu_usage = max(system_info["CPU Info"]["CPU Usage"])
        if cpu_usage > 80:
            response += " " + random.choice(witty_phrases["cpu"])

    # Ensure 'Memory Usage' is correctly accessed
    if "Memory Usage" in system_info:
        memory_usage = float(system_info["Memory Usage"][:-1])
        if memory_usage > 65:
            response += " " + random.choice(witty_phrases["memory"])

    # Check disk usage from 'Disk Info'
    if "Disk Info" in system_info:
        for disk in system_info["Disk Info"]:
            disk_usage = float(disk["Disk Usage"][:-1])
            if disk_usage > 90:
                response += " " + random.choice(witty_phrases["disk"])
                break  # Stop after the first occurrence

    # Ensure 'Network Status' is correctly accessed
    network_status = system_info.get("Network Status", "")
    if network_status == "Disconnected":
        response += " " + random.choice(witty_phrases["network"])

    # Ensure 'Battery Status' is correctly accessed
    battery_status = system_info.get("Battery Status", "")
    if battery_status == "Low":
        battery_response = random.choice(witty_phrases["battery"])
        if random.random() < 0.3:  # Adjust the probability as needed
            battery_response += " Sir."
        response += " " + battery_response

    return response


# Get live system information
def get_live_system_info():
    return get_system_info()


def get_live_system_status_response():
    info_system = get_live_system_info()
    return generate_system_status_response(info_system)


def get_live_storage_status_response():
    info_system = get_live_system_info()
    return generate_storage_status_response(info_system)


def get_live_cpu_usage_response():
    info_system = get_live_system_info()
    return generate_cpu_usage_response(info_system)


def get_live_memory_usage_response():
    info_system = get_live_system_info()
    return generate_memory_usage_response(info_system)


def get_live_disk_space_response():
    info_system = get_live_system_info()
    return generate_disk_space_response(info_system)


# Call these functions whenever you need the live system information.
system_info = get_live_system_status_response()
storage_info = get_live_storage_status_response()
cpu_usage = get_live_cpu_usage_response()
memory_usage = get_live_memory_usage_response()
disk_space = get_live_disk_space_response()
