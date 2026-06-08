"""System information collection."""
import platform, os, shutil, subprocess, sys

def get_os():
    return platform.system()

def get_arch():
    return platform.machine().lower()

def get_os_version():
    return f"{platform.system()} {platform.release()}"

def get_python_version():
    return sys.version.split()[0]

def get_disk_free_gb(path=None):
    if path is None:
        path = os.path.expanduser("~")
    return shutil.disk_usage(path).free // (1024**3)

def get_memory_gb():
    try:
        import psutil
        return psutil.virtual_memory().total // (1024**3)
    except ImportError:
        return -1

def get_cpu_count():
    return os.cpu_count() or -1

def check_command(cmd):
    return shutil.which(cmd) is not None

def run_command(cmd, timeout=10):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    except Exception as e:
        return -1, "", str(e)

def check_python_package(pkg):
    try:
        __import__(pkg.replace("-", "_"))
        return True
    except ImportError:
        return False
