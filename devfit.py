#!/usr/bin/env python
"""DevFit — Developer Environment Fitness Checker.
Usage: python devfit.py check <framework>
       python devfit.py fix <framework>
       python devfit.py list
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    if len(sys.argv) < 2:
        print("DevFit v0.1.0 — Developer Environment Fitness Checker")
        print()
        print("Usage:")
        print("  python devfit.py check <name>    Run environment check")
        print("  python devfit.py fix <name>      Auto-install missing deps")
        print("  python devfit.py list            List all profiles")
        print("  python devfit.py check --json <name>  JSON output")
        print()
        print("Examples:")
        print("  python devfit.py check hermes")
        print("  python devfit.py fix python")
        return

    cmd = sys.argv[1]
    
    if cmd == "list":
        from core.engine import Engine
        e = Engine()
        profiles = e.list_profiles()
        print(f"Available profiles ({len(profiles)}):")
        for p in profiles:
            print(f"  {p}")
        return

    if cmd == "check":
        name = sys.argv[2] if len(sys.argv) > 2 else ""
        if not name:
            print("Usage: python devfit.py check <framework>")
            return
        
        json_mode = "--json" in sys.argv
        if json_mode:
            name = [a for a in sys.argv[2:] if not a.startswith("--")][0] if len(sys.argv) > 2 else ""
        
        from core.engine import Engine
        e = Engine()
        reporter = e.check(name)
        if reporter:
            if json_mode:
                print(reporter.json())
            else:
                print(reporter.terminal())
        return

    if cmd == "fix":
        name = sys.argv[2] if len(sys.argv) > 2 else ""
        if not name:
            print("Usage: python devfit.py fix <framework>")
            return
        
        from core.engine import Engine
        e = Engine()
        e.fix(name)
        return

    print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
