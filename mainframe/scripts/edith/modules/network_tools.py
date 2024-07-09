import os
import subprocess
import socket
import sys
import ipaddress
import urllib.request
import time
from tkinter import Tk, simpledialog
import speedtest


def download_speed_test():

    output = ""
    st = speedtest.Speedtest()
    st.get_best_server()  # Find the best server based on ping

    print("Testing download speed...")
    download_speed = st.download() / 1024 / 1024  # Convert from bits to megabytes
    download_speed_str = f"{download_speed:.2f}".replace(".", " point ")
    output += f"Your download speed is about {download_speed_str} megabytes per second"

    # Upload speed test
    print("Testing upload speed...")
    upload_speed = st.upload() / 1024 / 1024  # Convert from bits to megabytes
    upload_speed_str = f"{upload_speed:.2f}".replace(".", " point ")
    output += (
        f" And your upload speed is around {upload_speed_str} megabytes per second, sir"
    )
    return output


def parse_ip_address(ip_str):
    try:
        # Check if the input is already a valid IPv4 address
        ip = ipaddress.IPv4Address(ip_str)
        return str(ip)
    except ipaddress.AddressValueError:
        # Try parsing spelled-out IP address
        parts = ip_str.split()
        if len(parts) == 4:
            try:
                ip = ".".join(str(int(part)) for part in parts)
                ipaddress.IPv4Address(ip)  # Validate the parsed IP
                return ip
            except (ValueError, ipaddress.AddressValueError):
                pass
        return None


def ping_ip(ip_str):
    ip = parse_ip_address(ip_str)
    if ip is None:
        return f"Invalid IP address format: {ip_str}"

    print(f"Pinging {ip}...")
    result = subprocess.call(["ping", ip])
    if result == 0:
        return f"Ping successful. {ip} is online, sir."
    else:
        return f"Ping failed. {ip} seems to be offline or unreachable."


# Function to get IP address input from user
def get_ip_address(prompt):
    root = Tk()
    root.withdraw()  # Hide the main window

    ip_address = simpledialog.askstring("Input", prompt)
    root.destroy()  # Destroy the main window after input dialog is closed

    return ip_address


def traffic_analysis():
    print("Analyzing network traffic...")
    # Placeholder for network traffic analysis


def extract_name(user_input, keyword):
    """
    Extracts the filename or folder name from the user input command.

    Args:
    user_input (str): User input command.
    keyword (str): Keyword to search for (e.g., 'named', 'labeled').

    Returns:
    str: Extracted name or None if not found.
    """
    parts = user_input.split(" ")
    try:
        index = parts.index(keyword)
        return " ".join(parts[index + 1 :])
    except ValueError:
        return None


def network_function(user_input):

    if (
        ("speedtest" or "speed test")
        and ("perform" in user_input or "test")
        and "network speed" in user_input
    ):
        download_speed_test()
    elif "ping" in user_input:
        ip = extract_name(user_input, "ping")

        ip = get_ip_address("Enter IP address to ping:")
        if ip:
            return ping_ip(ip)
        else:
            return "No IP address specified."

    elif "network" and "traffic" in user_input:
        traffic_analysis()
    else:
        print("Command not recognized.")
