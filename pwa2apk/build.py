#!/usr/bin/env python3
# PWA2APK - Trigger APK build via GitHub Actions

import argparse, os, sys, json, urllib.request

REPO = os.environ.get('GITHUB_REPOSITORY', 'yunqingtao/tiger')
TOKEN = os.environ.get('GITHUB_TOKEN', '')

def trigger(url, name, app_id):
    if not TOKEN:
        print('Set GITHUB_TOKEN env var first')
        sys.exit(1)
    api = 'https://api.github.com/repos/' + REPO + '/actions/workflows/build-apk.yml/dispatches'
    body = json.dumps({'ref':'main','inputs':{'url':url,'app_name':name,'app_id':app_id}}).encode()
    req = urllib.request.Request(api, data=body, method='POST')
    req.add_header('Authorization', 'Bearer ' + TOKEN)
    req.add_header('Accept', 'application/vnd.github+json')
    try:
        urllib.request.urlopen(req)
        print('OK: ' + name)
        print('https://github.com/' + REPO + '/actions')
    except Exception as e:
        print('FAIL: ' + str(e))

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--url', default='https://maryask.com/bot/')
    p.add_argument('--name', default='虎哥')
    p.add_argument('--id', default='com.maryask.huge')
    a = p.parse_args()
    trigger(a.url, a.name, a.id)