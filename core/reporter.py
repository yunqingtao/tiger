"""Report generation — terminal, JSON."""
import json
from datetime import datetime

class Reporter:
    def __init__(self, framework_name):
        self.name = framework_name
        self.sections = []
        self.total_pass = 0
        self.total_fail = 0
        self.total_warn = 0
        self.fixes = []

    def add_section(self, title, checks):
        self.sections.append({"title": title, "checks": checks})
        for _, status, _ in checks:
            if status == "pass": self.total_pass += 1
            elif status == "fail": self.total_fail += 1
            else: self.total_warn += 1

    def add_fix(self, item, cmd):
        self.fixes.append({"item": item, "cmd": cmd})

    def terminal(self):
        lines = []
        total = self.total_pass + self.total_fail + self.total_warn
        score = int(self.total_pass / total * 100) if total > 0 else 100
        
        lines.append("")
        lines.append("  \u2554" + "\u2550" * 56 + "\u2557")
        lines.append(f"  \u2551  DevFit \u00b7 {self.name} \u73af\u5883\u4f53\u68c0".ljust(59) + "\u2551")
        lines.append("  \u255a" + "\u2550" * 56 + "\u255d")
        lines.append("")

        for section in self.sections:
            lines.append(f"  [{section['title']}]")
            for label, status, detail in section["checks"]:
                icon = {"pass": "\u2713", "fail": "\u2717", "warn": "\u26a0"}.get(status, "?")
                line = f"    {icon} {label}"
                if detail:
                    line += f"  ({detail})"
                lines.append(line)
            lines.append("")

        lines.append("  " + "\u2500" * 56)
        lines.append(f"  \u7ed3\u679c: {self.total_pass}/{total} \u901a\u8fc7  [{self._bar(score)}] {score}%")
        if self.fixes:
            lines.append(f"  \u5f85\u4fee\u590d: {len(self.fixes)} \u9879")
            lines.append(f"  \u8fd0\u884c: devfit fix {self.name.lower()} \u4e00\u952e\u4fee\u590d")
        lines.append("  " + "\u2500" * 56)
        return "\n".join(lines)

    def json(self):
        total = self.total_pass + self.total_fail + self.total_warn
        return json.dumps({
            "framework": self.name,
            "timestamp": datetime.now().isoformat(),
            "score": int(self.total_pass / total * 100) if total > 0 else 100,
            "passed": self.total_pass, "failed": self.total_fail, "warnings": self.total_warn,
            "sections": self.sections, "fixes": self.fixes,
        }, ensure_ascii=False, indent=2)

    def _bar(self, pct, width=20):
        filled = int(pct / 100 * width)
        return "\u2588" * filled + "\u2591" * (width - filled)
