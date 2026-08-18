#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""SenseNova U1 Fast 文生图，自动下载到本地。"""
import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error

API = "https://token.sensenova.cn/v1/images/generations"
KEY = os.environ.get("SENSENOVA_API_KEY", "sk-B7flAfr3sCoFSY8U8HPscmF9pPQNC3of")
VALID_SIZES = {
    "1664x2496", "2496x1664", "1760x2368", "2368x1760",
    "1824x2272", "2272x1824", "2048x2048", "2752x1536",
    "1536x2752", "3072x1376", "1344x3136", "2560x720", "3072x864",
}


def post(payload):
    req = urllib.request.Request(
        API,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--size", default="2048x2048")
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--out", default="./generated-images")
    ap.add_argument("--no-watermark", action="store_true")
    a = ap.parse_args()

    if a.size not in VALID_SIZES:
        print("[ERR] size 非法: %s\n合法值: %s" % (a.size, ", ".join(sorted(VALID_SIZES))))
        sys.exit(1)

    payload = {
        "model": "sensenova-u1-fast",
        "prompt": a.prompt,
        "n": a.n,
        "size": a.size,
        "watermark": not a.no_watermark,
    }

    data = None
    for attempt in range(5):
        try:
            data = post(payload)
            break
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "ignore")
            if e.code == 429 and attempt < 4:
                wait = 2 ** attempt * 5
                print("[WARN] 429 限流，%ds 后重试 (%d/5)" % (wait, attempt + 1))
                time.sleep(wait)
                continue
            print("[ERR] HTTP %s: %s" % (e.code, body))
            sys.exit(1)

    if not data:
        print("[ERR] 重试耗尽")
        sys.exit(1)

    os.makedirs(a.out, exist_ok=True)
    ts = time.strftime("%Y%m%d%H%M%S")
    saved = []
    for i, item in enumerate(data.get("data", [])):
        url = item.get("url")
        if not url:
            continue
        path = os.path.join(a.out, "u1_%s_%d.png" % (ts, i))
        urllib.request.urlretrieve(url, path)
        saved.append(os.path.abspath(path))
        print("[OK] %s" % os.path.abspath(path))

    if not saved:
        print("[ERR] 无图片返回: %s" % json.dumps(data, ensure_ascii=False)[:500])
        sys.exit(1)


if __name__ == "__main__":
    main()
