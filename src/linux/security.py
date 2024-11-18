import socket
import ssl
import subprocess
from scapy.all import IP, TCP, sr1

class NetworkSecurityCheck:
    def __init__(self, target_ip):
        self.target_ip = target_ip

    @staticmethod
    def is_nmap_installed():
        try:
            result = subprocess.run(["nmap", "--version"], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def nmap_scan(target_ip):
        try:
            result = subprocess.run(["nmap", "-Pn", target_ip], capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return f"Error running nmap: {e}"

    def firewall_detection(target_ip, port):
        try:
            with socket.create_connection((target_ip, port), timeout=2) as sock:
                return f"Port {port} is open and reachable."
        except socket.timeout:
            return f"Port {port} seems filtered or blocked by a firewall."
        except ConnectionRefusedError:
            return f"Port {port} is closed but not filtered by a firewall."
        except Exception as e:
            return f"Error in firewall detection: {e}"

    def ssl_tls_inspection(hostname=None, port=443, target_ip='8.8.8.8'):
        hostname = hostname or target_ip
        result = {
            "hostname": hostname,
            "ssl_version": None,
            "certificate_valid": False,
            "issuer": None,
            "expiry_date": None,
            "subject": None,
            "error": None
        }

        try:
            context = ssl.create_default_context()
            with socket.create_connection((target_ip, port)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    result["ssl_version"] = ssock.version()
                    common_names = [entry[1] for entry in cert.get('subject', []) if entry[0] == 'commonName']
                    subject_alt_names = [san[1] for san in cert.get('subjectAltName', [])]

                    if hostname in common_names or hostname in subject_alt_names:
                        result["certificate_valid"] = True
                    result["issuer"] = ', '.join(f"{name[0]}={name[1]}" for name in cert.get("issuer", []))
                    result["expiry_date"] = cert.get("notAfter")
                    result["subject"] = ', '.join(f"{name[0]}={name[1]}" for name in cert.get("subject", []))
        except ssl.SSLCertVerificationError as e:
            result["error"] = f"SSL Certificate Verification Error: {e}"
        except socket.timeout:
            result["error"] = "Connection timed out."
        except ConnectionRefusedError:
            result["error"] = "Connection refused."
        except Exception as e:
            result["error"] = f"Unexpected error: {e}"

        return result
