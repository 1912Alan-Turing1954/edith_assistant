import platform
import subprocess
import time

def monitor_security_risks_linux():
    try:
        # Monitor SSH authentication failures on Linux
        ssh_log_file = '/var/log/auth.log'
        with subprocess.Popen(['tail', '-n', '50', ssh_log_file], stdout=subprocess.PIPE) as proc:
            for line in proc.stdout:
                if b'Failed password' in line:
                    print(f"Detected SSH authentication failure (Linux): {line.decode('utf-8').strip()}")

        # Monitor for changes in critical system files on Linux (example using auditd)
        auditd_output = subprocess.check_output(['auditctl', '-l'])
        print("Auditd Configuration (Linux):")
        print(auditd_output.decode('utf-8'))

        # Monitor network connections on Linux
        netstat_output = subprocess.check_output(['netstat', '-an'])
        print("Network Connections (Linux):")
        print(netstat_output.decode('utf-8'))

        # Add more Linux-specific monitoring here (e.g., process monitoring, file integrity checks)
        
    except Exception as e:
        print(f"Error in Linux monitoring: {e}")

def monitor_security_risks_windows():
    try:
        # Monitor Windows Event Logs for security events
        security_events = subprocess.check_output(['Get-WinEvent', '-LogName', 'Security', '-MaxEvents', '50'])
        print("Security Events (Windows):")
        print(security_events.decode('utf-8'))

        # Monitor for changes in critical system files on Windows (example using PowerShell)
        powershell_command = """
        Get-ChildItem -Path C:\\Windows\\System32 -Recurse | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) }
        """
        file_changes = subprocess.check_output(['powershell.exe', '-Command', powershell_command])
        print("File Changes (Windows):")
        print(file_changes.decode('utf-8'))

        # Monitor active network connections on Windows
        netstat_output = subprocess.check_output(['netstat', '-ano'])
        print("Network Connections (Windows):")
        print(netstat_output.decode('utf-8'))

        # Add more Windows-specific monitoring here (e.g., Sysmon logs, firewall status)
        
    except Exception as e:
        print(f"Error in Windows monitoring: {e}")

def main():
    while True:
        # Detect platform
        current_platform = platform.system()
        print(f"Running on {current_platform}")

        if current_platform == "Linux":
            monitor_security_risks_linux()
        elif current_platform == "Windows":
            monitor_security_risks_windows()

        # Sleep for some time before next iteration (adjust as per monitoring interval)
        time.sleep(60)  # Monitor every 1 minute


