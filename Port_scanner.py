import sys
import subprocess
import ctypes
import os

# --- 1. AUTO-INSTALLER ---
def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Library '{package}' not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Installation successful!\n")

install_and_import('psutil')

import psutil
import time
from datetime import datetime

# --- 2. ADMIN AUTO-ELEVATE ---
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    script_path = os.path.abspath(__file__)
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, f'"{script_path}"', None, 1
    )
    sys.exit()

# --- 3. BEAUTY & UI SETTINGS ---
# Colors (ANSI)
BLUE = "\033[94m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

def list_ports():
    # Enable ANSI support for Windows Command Prompt
    os.system('') 
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{CYAN}{BOLD}NETWORK PORT MONITOR{RESET}")
    print(f"{CYAN}Updated at: {datetime.now().strftime('%H:%M:%S')}{RESET}")
    print(f"{BLUE}=" * 100 + f"{RESET}")
    
    # Spread out headers
    print(f"{BOLD}{'PROTOCOL':<12} | {'LOCAL ADDRESS':<25} | {'PORT':<10} | {'STATUS':<15} | {'PROCESS (PID)'}{RESET}")
    print(f"{BLUE}-" * 100 + f"{RESET}")

    try:
        connections = psutil.net_connections(kind='inet')
        connections.sort(key=lambda x: x.laddr.port)

        for conn in connections:
            if conn.status in ['LISTEN', 'ESTABLISHED']:
                port = conn.laddr.port
                ip = conn.laddr.ip
                protocol = f"{BLUE}TCP{RESET}" if conn.type == 1 else f"{YELLOW}UDP{RESET}"
                
                # Highlight status
                status_color = GREEN if conn.status == 'LISTEN' else RESET
                status_text = f"{status_color}{conn.status:<15}{RESET}"
                
                try:
                    process = psutil.Process(conn.pid)
                    p_name = f"{CYAN}{process.name()}{RESET} ({conn.pid})"
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    p_name = f"System/Protected ({conn.pid})"
                
                # Spread out data rows
                print(f"{protocol:<21} | {ip:<25} | {port:<10} | {status_text} | {p_name}")
        
        print(f"{BLUE}=" * 100 + f"{RESET}")
        print(f"{YELLOW}Refreshing every 10 minutes... Press Ctrl+C to exit.{RESET}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        while True:
            list_ports()
            time.sleep(600) 
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Scanner stopped.{RESET}")
    except Exception as e:
        print(f"\nCrash Error: {e}")
        input("\nPress Enter to close...")