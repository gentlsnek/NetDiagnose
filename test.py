import socket
import platform
import subprocess
import speedtest
import time
from datetime import datetime
import csv
import os

class NetworkDiagnostics:
    def __init__(self):
        self.results_file = 'network_diagnostics.csv'
        self.initialize_results_file()
    
    def initialize_results_file(self):
        if not os.path.exists(self.results_file):
            with open(self.results_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Test Type', 'Result'])
    
    def ping_test(self, host="8.8.8.8", count=4):
        """Perform ping test to specified host"""
        try:
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            command = ['ping', param, str(count), host]
            output = subprocess.check_output(command).decode().strip()
            return True, output
        except subprocess.CalledProcessError:
            return False, "Ping test failed"
    
    def dns_lookup(self, domain="google.com"):
        """Perform DNS lookup for specified domain"""
        try:
            ip_address = socket.gethostbyname(domain)
            return True, f"DNS lookup successful. IP address: {ip_address}"
        except socket.gaierror:
            return False, "DNS lookup failed"
    
    def speed_test(self):
        """Perform internet speed test"""
        try:
            st = speedtest.Speedtest()
            print("Testing download speed...")
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            print("Testing upload speed...")
            upload_speed = st.upload() / 1_000_000  # Convert to Mbps
            return True, f"Download: {download_speed:.2f} Mbps, Upload: {upload_speed:.2f} Mbps"
        except Exception as e:
            return False, f"Speed test failed: {str(e)}"
    
    def port_scan(self, host="localhost", ports=[80, 443, 22, 21]):
        """Scan specific ports on the specified host"""
        results = []
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            if result == 0:
                results.append(f"Port {port} is open")
            sock.close()
        return True, "\n".join(results) if results else "No open ports found"
    
    def log_result(self, test_type, result):
        """Log test results to CSV file"""
        with open(self.results_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now(), test_type, result])
    
    def run_diagnostics(self):
        """Run all diagnostic tests"""
        print("Starting Network Diagnostics...")
        
        # Ping Test
        print("\nPerforming ping test...")
        success, ping_result = self.ping_test()
        self.log_result("Ping Test", ping_result)
        print(ping_result)
        
        # DNS Lookup
        print("\nPerforming DNS lookup...")
        success, dns_result = self.dns_lookup()
        self.log_result("DNS Lookup", dns_result)
        print(dns_result)
        
        # Speed Test
        print("\nPerforming speed test...")
        success, speed_result = self.speed_test()
        self.log_result("Speed Test", speed_result)
        print(speed_result)
        
        # Port Scan
        print("\nPerforming port scan...")
        success, port_result = self.port_scan()
        self.log_result("Port Scan", port_result)
        print(port_result)

if __name__ == "__main__":
    diagnostics = NetworkDiagnostics()
    diagnostics.run_diagnostics()