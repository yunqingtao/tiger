# DevFit

Developer Environment Fitness Checker — 一键式开发环境体检工具。

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 是什么

装任何开发框架之前跑一下，自动检测环境对不对、缺什么、装好没。

```
$ python devfit.py check hermes

  ╔══════════════════════════════════╗
  ║  DevFit · Hermes Agent 环境体检  ║
  ╚══════════════════════════════════╝

  [安装前 · 系统环境]
    ✓ 操作系统: Windows 11
    ✓ 架构: amd64
    ✓ Python: 3.13.13  (≥3.10)
    ✓ 磁盘: 80GB 可用
    ✓ 内存: 15GB

  [安装前 · 依赖项]
    ✓ Python包: websockets  已安装
    ✓ Python包: pyyaml  已安装
    ✗ Python包: playwright  未安装

  [端口检测]
    ✓ 端口 9222  可用

  [安装后 · 完整性]
    ✓ 可执行文件: hermes  已安装
    ✓ 版本验证  Hermes Agent v0.15.2

  [安装后 · 功能验证]
    ✓ 帮助命令  OK
    ✓ 状态检查  OK
    ✓ 技能列表  OK
    ✓ 对话测试  OK

  ───────────────────────────────────
  结果: 8/9 通过  [██████████████████░] 89%
  待修复: 1 项
  运行: devfit fix hermes 一键修复
  ───────────────────────────────────
```

## 支持框架（27个）

| 类别 | 框架 |
|------|------|
| AI Agent | Hermes, OpenClaw, LangChain, CrewAI, Ollama, Claude Code, Codex |
| 语言 | Python, Node.js, Go, Rust, Java |
| 浏览器 | Chrome, Playwright, Selenium |
| 数据库 | MySQL, PostgreSQL, Redis, SQLite |
| 运维 | Docker, nginx, PM2, Git |
| AI/ML | PyTorch, TensorFlow, CUDA, FFmpeg |

## 安装

```bash
git clone https://github.com/yunqingtao/devfit.git
cd devfit
pip install -r requirements.txt
```

## 使用

```bash
# 列出所有框架
python devfit.py list

# 体检
python devfit.py check hermes
python devfit.py check python
python devfit.py check docker

# JSON 输出（CI/CD）
python devfit.py check hermes --json

# 一键修复
python devfit.py fix hermes
```


## 国内镜像

`devfit fix` 自动检测网络，PyPI 慢时自动切换国内镜像：

| 源 | 镜像 |
|------|------|
| pip | 清华 → 阿里 → 中科大 → 豆瓣 → 华为 → 官方 |
| npm | 淘宝 → 腾讯 → 华为 → 官方 |

无需手动配置，全自动。

## 自定义框架

在 `profiles/` 下创建 YAML 文件即可，参考 `profiles/ai-agent/hermes.yaml`。

## 许可

MIT
