"""Auto-installer with mirror fallback for Chinese users."""
import subprocess, sys
from core.system import run_command, check_python_package

# Mirror sources — ordered by reliability in China
PYPI_MIRRORS = [
    ("清华", "https://pypi.tuna.tsinghua.edu.cn/simple"),
    ("阿里", "https://mirrors.aliyun.com/pypi/simple/"),
    ("中科大", "https://pypi.mirrors.ustc.edu.cn/simple/"),
    ("豆瓣", "https://pypi.douban.com/simple/"),
    ("华为", "https://repo.huaweicloud.com/repository/pypi/simple"),
    ("官方", "https://pypi.org/simple/"),
]

NPM_MIRRORS = [
    ("淘宝", "https://registry.npmmirror.com"),
    ("腾讯", "https://mirrors.cloud.tencent.com/npm/"),
    ("华为", "https://repo.huaweicloud.com/repository/npm/"),
    ("官方", "https://registry.npmjs.org/"),
]

APT_MIRRORS_UBUNTU = [
    ("阿里", "http://mirrors.aliyun.com/ubuntu/"),
    ("清华", "https://mirrors.tuna.tsinghua.edu.cn/ubuntu/"),
    ("中科大", "http://mirrors.ustc.edu.cn/ubuntu/"),
]

BREW_MIRRORS = [
    ("清华", "https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles"),
    ("中科大", "https://mirrors.ustc.edu.cn/homebrew-bottles"),
]


def install_python_package(pkg, verbose=True):
    """Install Python package with mirror fallback."""
    if check_python_package(pkg):
        return True, "already installed"

    for mirror_name, mirror_url in PYPI_MIRRORS:
        if verbose:
            print(f"    Trying {mirror_name} mirror...")
        rc, out, err = run_command(
            f'"{sys.executable}" -m pip install {pkg} -i {mirror_url} --trusted-host {mirror_url.split("/")[2]}',
            timeout=90
        )
        if rc == 0:
            if verbose:
                print(f"    ✓ {pkg} installed via {mirror_name}")
            return True, out

    return False, f"All mirrors failed for {pkg}"


def install_npm_package(pkg, verbose=True):
    """Install npm package with mirror fallback."""
    # Check if already installed
    rc, out, _ = run_command(f"npm list -g {pkg} --depth=0", timeout=10)
    if rc == 0 and pkg in out:
        return True, "already installed"

    for mirror_name, mirror_url in NPM_MIRRORS:
        if verbose:
            print(f"    Trying {mirror_name} npm mirror...")
        rc, out, err = run_command(
            f"npm install -g {pkg} --registry={mirror_url}",
            timeout=120
        )
        if rc == 0:
            if verbose:
                print(f"    ✓ {pkg} installed via {mirror_name}")
            return True, out

    return False, f"All npm mirrors failed for {pkg}"


def configure_pip_mirror():
    """One-time: configure pip to use Tsinghua mirror globally."""
    rc, out, _ = run_command(
        f'"{sys.executable}" -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple',
        timeout=15
    )
    return rc == 0


def configure_npm_mirror():
    """One-time: configure npm to use taobao mirror."""
    rc, out, _ = run_command(
        "npm config set registry https://registry.npmmirror.com",
        timeout=15
    )
    return rc == 0


def auto_configure_mirrors():
    """Detect if mirrors would help and configure them."""
    # Quick test: try pip install a tiny package from official
    rc, _, _ = run_command(
        f'"{sys.executable}" -m pip install --dry-run pip -i https://pypi.org/simple/ --trusted-host pypi.org',
        timeout=8
    )
    if rc != 0:
        print("  Detected slow PyPI access, configuring Tsinghua mirror...")
        configure_pip_mirror()
        return True
    return False


class Installer:
    @staticmethod
    def install(name, profile, verbose=True):
        """Install all missing dependencies for a framework."""
        deps = profile.get("dependencies", {})
        fixed = 0
        failed = []

        # Auto-configure mirrors first
        auto_configure_mirrors()

        # Python packages
        for pkg in deps.get("python", []):
            ok, msg = install_python_package(pkg, verbose)
            if ok:
                fixed += 1
            else:
                failed.append(f"pip:{pkg}")

        # npm packages
        for pkg in deps.get("npm", []):
            ok, msg = install_npm_package(pkg, verbose)
            if ok:
                fixed += 1
            else:
                failed.append(f"npm:{pkg}")

        # External tools
        for ext in deps.get("external", []):
            name = ext.get("name", "")
            check_cmd = ext.get("check", "")
            if check_cmd and check_python_package(check_cmd.split()[0]):
                continue  # Already installed (for Python-based tools)

            # Try install commands with mirrors where applicable
            import platform
            os_name = platform.system().lower()
            install_cmd = ext.get(f"install_{os_name}", ext.get("install", ""))
            
            if install_cmd:
                if verbose:
                    print(f"  Installing {name}...")
                rc, out, err = run_command(install_cmd, timeout=180)
                if rc == 0:
                    fixed += 1
                else:
                    failed.append(name)

        return fixed, failed
