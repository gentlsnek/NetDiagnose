import psutil
import subprocess
import re

def get_wireless_interface():
    interfaces = psutil.net_if_addrs()
    for interface_name in interfaces:
        if 'Wi-Fi' in interface_name or 'Wireless' in interface_name or 'wlan' in interface_name:
            return interface_name
    return None

# Function to retrieve Wi-Fi interface details using netsh
def get_iw_info():
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "interfaces"], universal_newlines=True)
        print("Wi-Fi Interface Info (via netsh):")
        return result
    except subprocess.CalledProcessError as e:
        return f"Error retrieving Wi-Fi interface info: {e}"

# Function to retrieve signal strength and quality
def get_wifi_signal_strength():
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "interfaces"], universal_newlines=True)
        signal_strength = re.search(r'Signal\s*:\s*(\d+)%', result)
        if signal_strength:
            return f"Signal Strength: {signal_strength.group(1)}% \n\n"
        else:
            return "Signal strength information not found."
    except subprocess.CalledProcessError as e:
        return f"Error retrieving Wi-Fi signal strength: {e}"

# Function to retrieve available Wi-Fi networks
def get_wifi_networks():
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "networks", "mode=Bssid"], universal_newlines=True)
        print("Available Wi-Fi Networks (via netsh): \n")
        
        networks = {}
        current_ssid = ""
        for line in result.splitlines():
            if "SSID" in line:
                current_ssid = line.split(":", 1)[1].strip()
                networks[current_ssid] = {}
            elif "Signal" in line:
                networks[current_ssid]["Signal"] = line.split(":", 1)[1].strip()
            elif "Channel" in line:
                networks[current_ssid]["Channel"] = line.split(":", 1)[1].strip()
            elif "Authentication" in line:
                networks[current_ssid]["Security"] = line.split(":", 1)[1].strip()
        
        # Print network details
        for ssid, info in networks.items():
            print(f"SSID: {ssid}, Signal Strength: {info.get('Signal', 'Unknown')}, \n"
                  f"Security: {info.get('Security', 'Unknown')}, Channel: {info.get('Channel', 'Unknown')} \n")
            
        # Calculate channel interference
        channels = {}
        for info in networks.values():
            channel = info.get("Channel")
            if channel:
                channels[channel] = channels.get(channel, 0) + 1
        
        print("\nChannel Interference:")
        for channel, count in channels.items():
            print(f"Channel {channel}: {count} networks")
            
    except subprocess.CalledProcessError as e:
        return f"Error retrieving Wi-Fi networks: {e}"


def get_wifi_info():
    try:
        # Run the netsh command to get Wi-Fi network information
        result = subprocess.check_output(["netsh", "wlan", "show", "networks", "mode=Bssid"], universal_newlines=True)
        
        networks = {}
        current_ssid = ""
        
        # Parse the output for each network and its properties
        for line in result.splitlines():
            if "SSID" in line:
                current_ssid = line.split(":", 1)[1].strip()
                if current_ssid not in networks:
                    networks[current_ssid] = {"Signal": None, "Security": None, "Channel": None, "BSSIDs": []}
            elif "Signal" in line:
                networks[current_ssid]["Signal"] = line.split(":", 1)[1].strip()
            elif "Channel" in line:
                networks[current_ssid]["Channel"] = line.split(":", 1)[1].strip()
            elif "Authentication" in line:
                networks[current_ssid]["Security"] = line.split(":", 1)[1].strip()
            elif "BSSID" in line:
                bssid = line.split(":", 1)[1].strip()
                networks[current_ssid]["BSSIDs"].append(bssid)

        # Construct formatted output string using f-strings
        formatted_output = "\nAvailable Wi-Fi Networks:\n"
        formatted_output += "\n".join(
            f"SSID: {ssid}\n"
            f"  Signal Strength: {info.get('Signal', 'Unknown')}\n"
            f"  Security: {info.get('Security', 'Unknown')}\n"
            f"  Channel: {info.get('Channel', 'Unknown')}\n"
            f"  BSSIDs: {', '.join(info['BSSIDs'])}\n"
            for ssid, info in networks.items()
        )

        return formatted_output

    except subprocess.CalledProcessError as e:
        return f"Error retrieving Wi-Fi networks: {e}"