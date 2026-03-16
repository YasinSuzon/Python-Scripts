import os
import subprocess
import re
import time
import ctypes
import sys
import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# --- ADMIN AUTO-ELEVATE ---
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("Requesting administrator privileges...")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

# --- NETWORK FUNCTIONS ---
def get_my_subnet():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ".".join(ip.split(".")[:-1])
    except:
        return "192.168.1"

def get_device_info(ip):
    # Ping the device
    response = os.system(f"ping -n 1 -w 300 {ip} > nul")
    if response == 0:
        # Get MAC
        mac = "Unknown"
        try:
            output = subprocess.check_output(["arp", "-a", ip], stderr=subprocess.DEVNULL).decode("ascii")
            mac_search = re.search(r"(([a-f0-9]{2}-){5}[a-f0-9]{2})", output, re.I)
            if mac_search:
                mac = mac_search.group(1).replace("-", ":").upper()
        except:
            pass
        
        # Get Name
        name = "Unknown"
        try:
            name = socket.gethostbyaddr(ip)[0]
        except:
            pass

        return {"ip": ip, "mac": mac, "name": name}
    return None

def run_scanner():
    subnet = get_my_subnet()
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Scanning LAN ({subnet}.1 to .254)...")
    
    ips = [f"{subnet}.{i}" for i in range(1, 255)]
    found_devices = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(get_device_info, ips)
        for res in results:
            if res:
                found_devices.append(res)
    
    # Display Results
    print("\n" + "="*70)
    print(f"{'IP Address':<15} | {'MAC Address':<18} | {'Device Name'}")
    print("-" * 70)
    
    if not found_devices:
        print("No devices found. Check your network connection.")
    else:
        for d in found_devices:
            print(f"{d['ip']:<15} | {d['mac']:<18} | {d['name']}")
    
    print("-" * 70)
    print(f"Total Devices Found: {len(found_devices)}") # The new line you requested
    print("="*70 + "\n")

# --- MAIN LOOP ---
try:
    while True:
        run_scanner()
        print("Scan finished. Waiting 10 minutes for next refresh...")
        print("Press Ctrl+C to stop.")
        time.sleep(600)
except KeyboardInterrupt:
    print("\nScanner stopped by user.")
