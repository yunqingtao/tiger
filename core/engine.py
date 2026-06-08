"""Check engine — run all checks from a profile."""
import yaml, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.system import get_os, get_arch, get_os_version, get_python_version
from core.system import get_disk_free_gb, get_memory_gb, get_cpu_count
from core.system import check_command, run_command, check_python_package
from core.ports import scan_ports
from core.reporter import Reporter

# Import name mapping (package name -> import name)
IMPORT_MAP = {
    "pyyaml": "yaml",
    "pillow": "PIL",
    "mysql-connector-python": "mysql.connector",
    "psycopg2": "psycopg2",
    "selenium": "selenium",
    "playwright": "playwright",
    "torch": "torch",
    "torchvision": "torchvision",
    "tensorflow": "tensorflow",
    "langchain": "langchain",
    "langchain-openai": "langchain_openai",
    "chromadb": "chromadb",
    "crewai": "crewai",
    "sqlite3": "sqlite3",
    "websockets": "websockets",
    "pip": "pip",
    "setuptools": "setuptools",
    "wheel": "wheel",
}

class Engine:
    def __init__(self):
        self.reporter = None

    def load_profile(self, name):
        """Load a framework profile by name."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        profiles_dir = os.path.join(base_dir, "profiles")
        
        # Search all category dirs
        for cat in ["ai-agent", "languages", "browsers", "databases", "devops", "aiml"]:
            path = os.path.join(profiles_dir, cat, f"{name}.yaml")
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
        
        # Also check root
        path = os.path.join(profiles_dir, f"{name}.yaml")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        
        return None

    def list_profiles(self):
        """List all available profiles."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        profiles_dir = os.path.join(base_dir, "profiles")
        profiles = []
        for cat in os.listdir(profiles_dir):
            cat_path = os.path.join(profiles_dir, cat)
            if os.path.isdir(cat_path):
                for f in os.listdir(cat_path):
                    if f.endswith('.yaml'):
                        profiles.append(f.replace('.yaml', ''))
        return sorted(profiles)

    def check(self, profile_name):
        """Run full check on a framework."""
        profile = self.load_profile(profile_name)
        if not profile:
            print(f"Error: profile '{profile_name}' not found")
            print(f"Available: {', '.join(self.list_profiles())}")
            return None

        self.reporter = Reporter(profile.get("name", profile_name))

        # ── Stage 1: System ──
        sys_cfg = profile.get("system", {})
        checks = []
        
        # OS check
        current_os = get_os()
        required_os = [o.lower() for o in sys_cfg.get("os", [])]
        if required_os:
            ok = current_os.lower() in required_os
            checks.append((f"操作系统: {get_os_version()}", 
                          "pass" if ok else "fail",
                          f"需要 {'/'.join(required_os)}" if not ok else ""))
        
        # Arch
        required_arch = [a.lower() for a in sys_cfg.get("arch", [])]
        current_arch = get_arch()
        if required_arch:
            ok = current_arch in required_arch or any(a in current_arch for a in required_arch)
            checks.append((f"架构: {current_arch}",
                          "pass" if ok else "fail",
                          f"需要 {'/'.join(required_arch)}" if not ok else ""))
        
        # Python version
        py_req = sys_cfg.get("python", "")
        if py_req:
            current = get_python_version()
            ok = self._version_ok(current, py_req)
            checks.append((f"Python: {current}",
                          "pass" if ok else "fail",
                          f"需要 {py_req}" if not ok else ""))
        
        # Disk
        disk_req = sys_cfg.get("disk_mb", 0)
        if disk_req:
            free = get_disk_free_gb()
            ok = free >= disk_req // 1024
            checks.append((f"磁盘: {free}GB 可用",
                          "pass" if ok else "fail",
                          f"需要 {disk_req//1024}GB" if not ok else ""))
        
        # Memory
        mem_req = sys_cfg.get("memory_mb", 0)
        if mem_req:
            mem = get_memory_gb()
            if mem > 0:
                ok = mem >= mem_req // 1024
                checks.append((f"内存: {mem}GB",
                              "pass" if ok else "fail",
                              f"需要 {mem_req//1024}GB" if not ok else ""))
        
        self.reporter.add_section("安装前 · 系统环境", checks)

        # ── Stage 2: Dependencies ──
        deps = profile.get("dependencies", {})
        dep_checks = []
        fixes = []
        
        # Python packages
        for pkg in deps.get("python", []):
            import_name = IMPORT_MAP.get(pkg.lower(), pkg.replace("-", "_"))
            ok = check_python_package(import_name) if import_name else False
            dep_checks.append((f"Python包: {pkg}",
                              "pass" if ok else "fail",
                              "已安装" if ok else "未安装"))
            if not ok:
                fixes.append((pkg, f"pip install {pkg}"))
                self.reporter.add_fix(pkg, f"pip install {pkg}")
        
        # External commands
        for ext in deps.get("external", []):
            name = ext.get("name", ext.get("check", ""))
            cmd = ext.get("check", "")
            # Try multiple paths for the command
            cmd_name = cmd.split()[0]
            ok = check_command(cmd_name)
            if not ok and get_os() == "Windows":
                # Try full Chrome path on Windows
                chrome_paths = [
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                ]
                for cp in chrome_paths:
                    if os.path.exists(cp) and cmd_name in cp:
                        ok = True
                        break
            
            # Try running version check
            detail = ""
            if ok:
                rc, out, _ = run_command(cmd, timeout=5)
                if rc == 0 and out:
                    detail = out[:60]
            
            dep_checks.append((f"外部工具: {name}",
                              "pass" if ok else "fail",
                              detail if ok else "未安装"))
            if not ok:
                install_cmd = ext.get(f"install_{get_os().lower()}", ext.get("install", ""))
                if install_cmd:
                    self.reporter.add_fix(name, install_cmd)
        
        self.reporter.add_section("安装前 · 依赖项", dep_checks)

        # ── Stage 3: Ports ──
        ports = profile.get("ports", [])
        if ports:
            port_results = scan_ports(ports)
            port_checks = []
            for port, status in port_results.items():
                ok = status == "free"
                port_checks.append((f"端口 {port}",
                                   "pass" if ok else "warn",
                                   "可用" if ok else status))
            self.reporter.add_section("端口检测", port_checks)

        # ── Stage 4: Installation ──
        inst = profile.get("installation", {})
        inst_checks = []
        
        binary = inst.get("binary", "")
        if binary:
            ok = check_command(binary)
            inst_checks.append((f"可执行文件: {binary}",
                               "pass" if ok else "fail",
                               "已安装" if ok else "未找到"))
            if not ok:
                self.reporter.add_fix(binary, "请先安装该框架")
        
        version_cmd = inst.get("version_cmd", "")
        if version_cmd and check_command(version_cmd.split()[0]):
            rc, out, _ = run_command(version_cmd, timeout=10)
            if rc == 0:
                inst_checks.append(("版本验证",
                                   "pass",
                                   out.split(chr(10))[0][:60]))
        
        self.reporter.add_section("安装后 · 完整性", inst_checks)

        # ── Stage 5: Functionality ──
        funcs = profile.get("functionality", [])
        func_checks = []
        for fn in funcs:
            name = fn.get("name", "")
            cmd = fn.get("cmd", "")
            expect_rc = fn.get("expect_rc", 0)
            timeout = fn.get("timeout", 10)
            
            if not check_command(cmd.split()[0]):
                func_checks.append((name, "fail", "命令不可用"))
                continue
            
            rc, out, err = run_command(cmd, timeout=timeout)
            if rc == expect_rc:
                detail = (out or err)[:60] if out or err else "OK"
                func_checks.append((name, "pass", detail))
            else:
                func_checks.append((name, "fail", err[:60] if err else f"rc={rc}"))
        
        if func_checks:
            self.reporter.add_section("安装后 · 功能验证", func_checks)

        # ── Stage 6: Skills/Plugins ──
        skills = profile.get("skills", [])
        if skills:
            skill_checks = []
            for sk in skills:
                name = sk.get("name", "")
                check = sk.get("check", "")
                ok = False
                if check:
                    # If it's a Python import check, use mapping
                    if check.startswith("python -c"):
                        import re
                        m = re.search(r'import\s+(\S+)', check)
                        if m:
                            pkg_name = m.group(1)
                            mapped = IMPORT_MAP.get(pkg_name, pkg_name)
                            check2 = check.replace(f"import {pkg_name}", f"import {mapped}")
                            rc, out, _ = run_command(check2, timeout=10)
                        else:
                            rc, out, _ = run_command(check, timeout=10)
                    else:
                        rc, out, _ = run_command(check, timeout=10)
                    ok = (rc == 0)
                skill_checks.append((f"Skill: {name}",
                                    "pass" if ok else "fail",
                                    "已安装" if ok else "未安装"))
                if not ok:
                    install = sk.get("install", "")
                    if install:
                        self.reporter.add_fix(name, install)
            self.reporter.add_section("Skill / 插件", skill_checks)

        return self.reporter

    def fix(self, profile_name):
        """Auto-install missing dependencies with mirror fallback."""
        profile = self.load_profile(profile_name)
        if not profile:
            print(f"Profile '{profile_name}' not found")
            return
        
        from core.installer import Installer
        
        name = profile.get('name', profile_name)
        print(f"\n  Fixing {name}...")
        print(f"  (自动切换国内镜像)\n")
        
        fixed, failed = Installer.install(name, profile)
        
        print(f"\n  Fixed: {fixed} | Failed: {len(failed)}")
        if failed:
            print(f"  Failed items: {', '.join(failed)}")
            print(f"  Tip: 手动安装或检查网络连接")
        
        print(f"\n  Run 'devfit check {profile_name}' to verify.")

    def _version_ok(self, current, requirement):
        """Simple version check like '>=3.10'."""
        import re
        op = re.match(r'([<>=!]+)', requirement)
        if not op:
            return True
        op = op.group(1)
        req_ver = requirement.replace(op, '').strip()
        
        cur_parts = [int(x) for x in current.split('.')[:3]]
        req_parts = [int(x) for x in req_ver.split('.')[:3]]
        
        while len(cur_parts) < len(req_parts):
            cur_parts.append(0)
        while len(req_parts) < len(cur_parts):
            req_parts.append(0)
        
        if op == '>=': return cur_parts >= req_parts
        if op == '>': return cur_parts > req_parts
        if op == '<=': return cur_parts <= req_parts
        if op == '<': return cur_parts < req_parts
        if op == '==': return cur_parts == req_parts
        return True
