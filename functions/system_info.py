import psutil
import platform
import socket

def get_system_info():
    system_info = {}
    
    # Operating System
    system_info['Operating System'] = f"{platform.system()} {platform.release()}"
    
    # Computer Name
    system_info['Computer Name'] = psutil.users()[0].name
    
    # CPU Information
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    system_info['CPU Info'] = {
        'Physical Cores': psutil.cpu_count(logical=False),
        'Total Cores': psutil.cpu_count(logical=True),
        'CPU Usage': cpu_usage
    }

    # Memory Information
    memory = psutil.virtual_memory()
    system_info['Total Memory'] = f"{round(memory.total / (1024 ** 3), 2)} GB"
    system_info['Available Memory'] = f"{round(memory.available / (1024 ** 3), 2)} GB"
    system_info['Used Memory'] = f"{round(memory.used / (1024 ** 3), 2)} GB"
    system_info['Memory Usage'] = f"{memory.percent}%"

    # Disk Information
    partitions = psutil.disk_partitions(all=False)
    system_info['Disk Info'] = []
    for partition in partitions:
        partition_usage = psutil.disk_usage(partition.mountpoint)
        system_info['Disk Info'].append({
            'Drive': partition.device,
            'Mount Point': partition.mountpoint,
            'File System': partition.fstype,
            'Total Space': f"{round(partition_usage.total / (1024 ** 3), 2)} GB",
            'Used Space': f"{round(partition_usage.used / (1024 ** 3), 2)} GB",
            'Free Space': f"{round(partition_usage.free / (1024 ** 3), 2)} GB",
            'Disk Usage': f"{partition_usage.percent}%"
        })

    # Network Information
    network_info = psutil.net_if_addrs()
    system_info['Network Info'] = []
    for interface, addresses in network_info.items():
        for address in addresses:
            if address.family == socket.AF_INET:
                system_info['Network Info'].append({
                    'Interface': interface,
                    'IP Address': address.address,
                    'Netmask': address.netmask
                })
                break

    return system_info

def generate_system_status_response(system_info):
    response = "I have extracted your machine details, "
    cpu_usage = max(system_info['CPU Info']['CPU Usage'])
    memory_usage = float(system_info['Memory Usage'][:-1])
    overall_wellbeing = "good"

    if cpu_usage > 80:
        overall_wellbeing = "concerned"
        response += "I must inform you that your CPU usage is quite high at the moment. "
        response += "It would be advisable to close some unnecessary programs or tasks to improve performance."

    if memory_usage < 30:
        overall_wellbeing = "concerned"
        response += "Additionally, your available memory is running low. "
        response += "I suggest closing unused applications or considering an upgrade to your RAM for better multitasking."

    if overall_wellbeing == "good":
        response += "Overall, your PC is performing optimally, Should you require any further assistance or have inquiries, feel free to ask."
    else:
        response += "I am a tad concerned about your PC's performance. It would be prudent to follow the aforementioned recommendations to enhance its overall health and performance."

    return response

def generate_storage_status_response(system_info):
    response = "I have obtained your storage details. "
    free_disk_space = (system_info['Disk Info'][0]['Free Space'])
    free_disk_space = free_disk_space.replace("GB", "gigabytes")
    disk_usage = float(system_info['Disk Info'][0]['Disk Usage'][:-1])
    overall_wellbeing = "healthy"
    
    if disk_usage > 75:
        overall_wellbeing = "concerned"
        response += "I must express my concern as your PC's storage is currently under considerable strain. "
        response += "To ensure optimal performance, it is highly advisable to uninstall any unnecessary programs or games that are taking up excessive space."

    # New recommendation
    if disk_usage < 50:
        overall_wellbeing = "healthy"
        response += "Your PC's storage is functioning optimally. However, to maintain its peak performance, consider organizing your files and folders through defragmentation or rearranging data based on usage frequency."

    if overall_wellbeing == "healthy":
        response += f"At the moment, your PC has {free_disk_space} of free space, and your storage usage is at {disk_usage}%."
    else:
        response += "I am a tad concerned about your PC's storage health. It would be prudent to follow the aforementioned recommendations to enhance its overall storage performance."

    return response

# Get live system information
system_info = get_system_info()

info_system = generate_system_status_response(system_info)
storage_info = generate_storage_status_response(system_info)

