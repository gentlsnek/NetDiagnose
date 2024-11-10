import subprocess
import socket

def ping_test(destination):
    try:
        # Ping the destination
        result = subprocess.run(["ping", "-n", "10", destination], capture_output=True, text=True, timeout=100)
        if result.returncode == 0:
            print(f"Ping to {destination} successful.")
        else:
            print(f"Ping to {destination} failed.")
        return(result.stdout)
    except subprocess.TimeoutExpired:
        return(f"Ping to {destination} timed out.")
    except Exception as e:
        return(f"An error occurred during ping: {e}")


def dns_lookup(domain):
    try:
        # DNS lookup for the given domain
        print(f"DNS lookup for {domain}:")
        ip_address = socket.gethostbyname(domain)
        return(f"{domain} has IP address {ip_address}")
    except socket.gaierror:
        return(f"Failed to resolve DNS for {domain}")
    except Exception as e:
        return(f"An error occurred during DNS lookup: {e}")


def trace_route(destination):
    try:
       # print(f"Tracing route to {destination}:\n")
        result = subprocess.run(["tracert","-d","-w", "100", destination], capture_output=True, text=True, timeout=100)
        if result.returncode == 0:
            return(result.stdout)
        else:
            return(f"Trace route to {destination} failed.")
    except subprocess.TimeoutExpired:
        return(f"Tracing route to {destination} timed out.")
    except FileNotFoundError:
        return("The 'tracert' command is not found on this system.")
    except Exception as e:
        return(f"An error occurred during trace route: {e}")
