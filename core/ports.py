"""Port availability scanner."""
import socket, subprocess

def check_port(port, host="127.0.0.1"):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        result = sock.connect_ex((host, port))
        return result != 0
    except:
        return None
    finally:
        sock.close()

def get_port_process(port):
    try:
        r = subprocess.run(f'netstat -ano | findstr ":{port} "', 
                          shell=True, capture_output=True, text=True, timeout=5)
        if r.stdout.strip():
            parts = r.stdout.strip().split()
            pid = parts[-1] if parts else "?"
            return f"PID {pid}"
    except:
        pass
    return "unknown"

def scan_ports(port_list):
    results = {}
    for port in port_list:
        available = check_port(port)
        if available is None:
            results[port] = "error"
        elif available:
            results[port] = "free"
        else:
            results[port] = f"in_use ({get_port_process(port)})"
    return results
