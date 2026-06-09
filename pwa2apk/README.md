# PWA2APK — 虎哥打包工具

一键将任何 PWA/网页打包为 Android APK。

**原理**: GitHub Actions + Capacitor，云端编译，无需本地环境。

## 快速开始

### 1. 放到你的 GitHub 仓库

```bash
git init && git add . && git commit -m "pwa2apk"
git remote add origin https://github.com/你的用户名/pwa2apk.git
git push -u origin main
```

### 2. 设置 Token

GitHub → Settings → Developer settings → Personal access tokens → Tokens(classic)
勾选 `repo` + `workflow` 权限，生成 token。

```bash
# Windows
set GITHUB_TOKEN=ghp_xxxx
# Mac/Linux
export GITHUB_TOKEN=ghp_xxxx
```

### 3. 一键打包

```bash
# 默认打包虎哥对话
python build.py

# 自定义 URL
python build.py --url https://example.com --name 我的App --id com.example.app
```

### 4. 下载 APK

等3-5分钟 → GitHub Actions 跑完 → Artifacts 里下载 APK → 传到手机安装

## 或直接在 GitHub 网页操作

Actions → Build APK → Run workflow → 填参数 → 跑完下载
