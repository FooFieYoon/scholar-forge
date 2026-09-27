#!/usr/bin/env python3
"""
Agnes AI Image & Video Generation Script

Usage:
    # Image generation (text-to-image)
    python agnes-ai.py image --prompt "a cute cat" --size 1K --ratio 16:9 --output-dir ./output

    # Image generation (Base64)
    python agnes-ai.py image --prompt "a cute cat" --size 1K --ratio 16:9 --output-format b64

    # Image-to-image / multi-image composition
    python agnes-ai.py image --prompt "Transform into a cyberpunk neon style" \
        --image "https://example.com/input.jpg" --size 1024x768

    # Video generation (text-to-video)
    python agnes-ai.py video --prompt "a cat walking on the beach" --seconds 5 --size 720P --aspect-ratio 16:9

    # Video generation (image-to-video, keyframe)
    python agnes-ai.py video --prompt "person turns around" --image "https://example.com/photo.jpg" --mode keyframe

    # Video result query
    python agnes-ai.py video-query --video-id "video_xxx"

    # Polling video (auto-wait)
    python agnes-ai.py video --prompt "..." --poll --max-wait 600

    # 指定站点（中国站 / 国际站）方式一：命令行
    python agnes-ai.py --api-base https://api.agnes-ai.cn/v1 video --prompt "..." --poll

    # 指定站点方式二：环境变量 AGNES_API_BASE / AGNES_BASE_URL（写入 <SKILL_DIR>/.env）

API Reference:
    Image:  https://agnes-ai.com/doc/agnes-image-25-flash
    Video:  https://agnes-ai.com/zh-Hans/docs/agnes-video-25-flash

Models (both FREE as of 2026-09):
    Image:  agnes-image-2.5-flash
    Video:  agnes-video-2.5-flash  (free 720P; text / keyframe / reference modes)

API Base URL (站点，可切换):
    国际站（默认）: https://apihub.agnes-ai.com/v1
    中国站:        https://api.agnes-ai.cn/v1
    通过环境变量 AGNES_API_BASE / AGNES_BASE_URL 或命令行 --api-base 切换，
    脚本会自动适配对应的视频查询域名，无需改任何代码。
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path


def load_env_file(env_path):
    """手动加载 .env 文件（不依赖 python-dotenv 库）"""
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and not os.environ.get(key):
                        os.environ[key] = value


# 尝试从脚本同目录加载 .env
script_dir = os.path.dirname(os.path.abspath(__file__))
load_env_file(os.path.join(script_dir, '.env'))
load_env_file(os.path.join(script_dir, '..', '.env'))


# ===== 站点 / 模型默认值（运行时可由环境变量或命令行覆盖）=====
IMAGE_MODEL_DEFAULT = "agnes-image-2.5-flash"
VIDEO_MODEL_DEFAULT = "agnes-video-2.5-flash"
API_BASE_DEFAULT = "https://apihub.agnes-ai.com/v1"   # 国际站（默认）
QUERY_PATH = "/agnesapi"

# 以下全局变量在 main() 中根据环境变量 / 命令行参数确定最终值
API_BASE = API_BASE_DEFAULT
VIDEO_QUERY_BASE = "https://apihub.agnes-ai.com/agnesapi"  # 占位，main 中重算
IMAGE_MODEL = IMAGE_MODEL_DEFAULT
VIDEO_MODEL = VIDEO_MODEL_DEFAULT


def resolve_api_base():
    """确定图片/视频创建接口的 Base URL。

    优先级：命令行 --api-base > 环境变量 AGNES_API_BASE > 环境变量 AGNES_BASE_URL > 默认（国际站）。
    """
    base = (os.environ.get("AGNES_API_BASE")
            or os.environ.get("AGNES_BASE_URL")
            or API_BASE_DEFAULT)
    return base.rstrip("/")


def resolve_query_base(base):
    """根据 create base 推导视频查询域名。

    base 形如 https://apihub.agnes-ai.com/v1 -> 查询 https://apihub.agnes-ai.com/agnesapi。
    可用环境变量 AGNES_QUERY_BASE 强制覆盖（当查询域名与创建域名不一致时）。
    """
    override = os.environ.get("AGNES_QUERY_BASE")
    if override:
        return override.rstrip("/")
    if base.endswith("/v1"):
        host = base[:-3]
    else:
        host = base
    return host + QUERY_PATH


def get_api_key():
    """Read API key from AGNES_API_KEY environment variable."""
    key = os.environ.get("AGNES_API_KEY", "").strip()
    if not key:
        print(json.dumps({"error": "API_KEY_NOT_FOUND", "message": "AGNES_API_KEY environment variable is not set."}), file=sys.stderr)
        sys.exit(1)
    return key


def api_request(endpoint, method="POST", body=None, api_key=None, query_params=None):
    """Make an API request to Agnes AI."""
    if api_key is None:
        api_key = get_api_key()

    url = f"{API_BASE}/{endpoint}"
    if query_params:
        url += "?" + query_params

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        try:
            err_body = json.loads(body_text)
            print(json.dumps({"error": str(e.code), "message": err_body.get("message", body_text)}), file=sys.stderr)
        except json.JSONDecodeError:
            print(json.dumps({"error": str(e.code), "message": body_text}), file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(json.dumps({"error": "NETWORK", "message": str(e.reason)}), file=sys.stderr)
        sys.exit(1)


def generate_image(args):
    """Generate image using agnes-image-2.5-flash."""
    api_key = get_api_key()

    body = {
        "model": IMAGE_MODEL,
        "prompt": args.prompt,
        "size": args.size,
    }

    if hasattr(args, "ratio") and args.ratio:
        body["ratio"] = args.ratio

    # 图生图 / 多图合成：通过 extra_body.image 传入图片数组
    if hasattr(args, "image") and args.image:
        extra = {"image": [args.image]}
        if hasattr(args, "output_format") and args.output_format == "b64":
            extra["response_format"] = "b64_json"
        body["extra_body"] = extra
    elif hasattr(args, "output_format") and args.output_format == "b64":
        body["return_base64"] = True

    result = api_request("images/generations", body=body, api_key=api_key)

    # Extract result
    if "data" in result and result["data"]:
        item = result["data"][0]
        url = item.get("url")
        b64 = item.get("b64_json")
        revised = item.get("revised_prompt")

        output_dir = Path(args.output_dir) if hasattr(args, "output_dir") and args.output_dir else Path(".")
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if b64 and not url:
            # Base64 output
            ext = "png"
            out_path = output_dir / f"agnes_image_{timestamp}.{ext}"
            with open(out_path, "wb") as f:
                f.write(base64.b64decode(b64))
            print(json.dumps({
                "status": "success",
                "path": str(out_path),
                "revised_prompt": revised
            }))
        elif url:
            # URL output - download it
            out_path = output_dir / f"agnes_image_{timestamp}.png"
            try:
                with urllib.request.urlopen(url, timeout=60) as resp:
                    data = resp.read()
                with open(out_path, "wb") as f:
                    f.write(data)
                print(json.dumps({
                    "status": "success",
                    "path": str(out_path),
                    "url": url,
                    "revised_prompt": revised
                }))
            except Exception as e:
                print(json.dumps({
                    "status": "url_returned",
                    "url": url,
                    "download_error": str(e),
                    "revised_prompt": revised
                }))
        else:
            print(json.dumps({"error": "NO_OUTPUT", "response": result}))
    else:
        print(json.dumps({"error": "EMPTY_RESPONSE", "response": result}))


def generate_video(args):
    """Generate video using agnes-video-2.5-flash (async)."""
    api_key = get_api_key()

    # 图生视频便捷写法：单独传入 --image 时，自动转为 keyframe 首帧
    mode = args.mode
    if args.image and mode == "text" and not args.first_frame and not args.last_frame and not args.images:
        mode = "keyframe"
        args.first_frame = args.image

    body = {
        "model": VIDEO_MODEL,
        "prompt": args.prompt,
        "mode": mode,
        "seconds": str(args.seconds),
        "size": args.size,
        "aspect_ratio": args.aspect_ratio,
    }

    if args.seed is not None:
        body["seed"] = args.seed

    if args.negative_prompt:
        body["negative_prompt"] = args.negative_prompt

    if mode == "keyframe":
        if args.first_frame:
            body["first_frame"] = args.first_frame
        if args.last_frame:
            body["last_frame"] = args.last_frame
    elif mode == "reference":
        images = []
        if args.image:
            images.append(args.image)
        if args.images:
            images.extend([u.strip() for u in args.images.split(",") if u.strip()])
        if images:
            body["images"] = images
        if args.audios:
            body["audios"] = [u.strip() for u in args.audios.split(",") if u.strip()]

    result = api_request("videos", body=body, api_key=api_key)

    if "video_id" not in result:
        print(json.dumps({"error": "NO_VIDEO_ID", "response": result}))
        return

    video_id = result["video_id"]
    task_id = result.get("task_id", video_id)

    if hasattr(args, "poll") and args.poll:
        max_wait = getattr(args, "max_wait", 600)
        poll_interval = getattr(args, "poll_interval", 5)
        _poll_video(video_id, task_id, max_wait, poll_interval, args)
    else:
        print(json.dumps({
            "status": "submitted",
            "video_id": video_id,
            "task_id": task_id,
            "model": VIDEO_MODEL,
            "message": "Video generation task submitted. Use video-query --video-id to poll for results, or rerun with --poll."
        }))


def _poll_video(video_id, task_id, max_wait, poll_interval, args):
    """Poll for video result until completion or timeout."""
    api_key = get_api_key()
    start = time.time()
    output_dir = Path(args.output_dir) if hasattr(args, "output_dir") and args.output_dir else Path(".")
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    while time.time() - start < max_wait:
        # 2.5 系列必须使用 video_id + model_name 查询（站点无关）
        url = f"{VIDEO_QUERY_BASE}?video_id={video_id}&model_name={VIDEO_MODEL}"
        headers = {"Authorization": f"Bearer {api_key}"}
        req = urllib.request.Request(url, headers=headers, method="GET")

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            print(json.dumps({"error": f"POLL_HTTP_{e.code}", "message": e.read().decode()}), file=sys.stderr)
            time.sleep(poll_interval)
            continue
        except Exception as e:
            print(json.dumps({"error": "POLL_ERROR", "message": str(e)}), file=sys.stderr)
            time.sleep(poll_interval)
            continue

        status = result.get("status", "unknown")
        progress = result.get("progress", 0)
        print(f"  [poll] status={status}, progress={progress}%", file=sys.stderr)

        if status == "completed":
            # 2.5 系列：视频地址位于响应顶层 url 字段（站点无关）
            video_url = result.get("url") or (result.get("metadata", {}) or {}).get("url")
            if video_url:
                out_path = output_dir / f"agnes_video_{timestamp}.mp4"
                try:
                    with urllib.request.urlopen(video_url, timeout=120) as resp:
                        data = resp.read()
                    with open(out_path, "wb") as f:
                        f.write(data)
                    print(json.dumps({
                        "status": "success",
                        "path": str(out_path),
                        "url": video_url,
                        "size": result.get("size"),
                        "seconds": result.get("seconds")
                    }))
                except Exception as e:
                    print(json.dumps({
                        "status": "url_returned",
                        "url": video_url,
                        "download_error": str(e)
                    }))
            else:
                print(json.dumps({"error": "NO_URL", "response": result}))
            return

        if status == "failed":
            print(json.dumps({"error": "GENERATION_FAILED", "response": result}))
            return

        if status in ("queued", "in_progress"):
            time.sleep(poll_interval)
            continue

        # Unknown status, wait a bit
        time.sleep(poll_interval)

    print(json.dumps({"error": "TIMEOUT", "video_id": video_id, "max_wait": max_wait}))


def query_video(args):
    """Query video result by video_id (one-shot, no polling)."""
    api_key = get_api_key()
    video_id = args.video_id

    # 2.5 系列必须使用 video_id + model_name 查询（站点无关）
    url = f"{VIDEO_QUERY_BASE}?video_id={video_id}&model_name={VIDEO_MODEL}"
    headers = {"Authorization": f"Bearer {api_key}"}
    req = urllib.request.Request(url, headers=headers, method="GET")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(json.dumps({"error": f"QUERY_HTTP_{e.code}", "message": e.read().decode()}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": "QUERY_ERROR", "message": str(e)}), file=sys.stderr)
        sys.exit(1)

    status = result.get("status", "unknown")
    if status == "completed":
        video_url = result.get("url") or (result.get("metadata", {}) or {}).get("url")
        if video_url:
            output_dir = Path(args.output_dir) if hasattr(args, "output_dir") and args.output_dir else Path(".")
            output_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_path = output_dir / f"agnes_video_{timestamp}.mp4"
            try:
                with urllib.request.urlopen(video_url, timeout=120) as resp:
                    data = resp.read()
                with open(out_path, "wb") as f:
                    f.write(data)
                result["status"] = "success"
                result["path"] = str(out_path)
            except Exception as e:
                result["download_error"] = str(e)
    print(json.dumps(result))


def main():
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--api-base", default=None,
                        help="Agnes API base URL. 国际站(默认): https://apihub.agnes-ai.com/v1 ; "
                             "中国站: https://api.agnes-ai.cn/v1 . 也可用 .env 的 AGNES_API_BASE / AGNES_BASE_URL 设置。")

    parser = argparse.ArgumentParser(description="Agnes AI Image & Video Generation CLI", parents=[parent])
    sub = parser.add_subparsers(dest="command", required=True)

    # Image command
    img_parser = sub.add_parser("image", help="Generate image from text or image")
    img_parser.add_argument("--prompt", required=True, help="Text prompt for image generation")
    img_parser.add_argument("--size", default="1K",
                            help="Output size: 1K, 2K, 3K, 4K, or custom like 1024x768 (default: 1K)")
    img_parser.add_argument("--ratio", default="1:1",
                            help="Aspect ratio: 1:1, 16:9, 9:16, 4:3, 3:4, 2:3, 3:2, 21:9 (default: 1:1)")
    img_parser.add_argument("--image", help="Input image URL for image-to-image / multi-image composition")
    img_parser.add_argument("--output-format", choices=["url", "b64"], default="url",
                            help="Output format: url (default) or b64 (base64)")
    img_parser.add_argument("--output-dir", default=".", help="Directory to save output files")

    # Video command
    vid_parser = sub.add_parser("video", help="Generate video from text or image")
    vid_parser.add_argument("--prompt", required=True, help="Text prompt for video generation")
    vid_parser.add_argument("--mode", choices=["text", "keyframe", "reference"], default="text",
                            help="Generation mode: text (default), keyframe (首/尾帧), reference (图片/音频参考)")
    vid_parser.add_argument("--seconds", default="5",
                            help="Video duration in seconds, string \"4\"-\"12\" (default: 5)")
    vid_parser.add_argument("--size", default="720P",
                            help="Output resolution tier: 720P (default, Flash only), 1080P, 1K, 2K")
    vid_parser.add_argument("--aspect-ratio", default="16:9",
                            help="Aspect ratio: 16:9, 9:16, 1:1, 4:3, 3:4, 21:9 (default: 16:9)")
    vid_parser.add_argument("--seed", type=int, help="Random seed for reproducible results")
    vid_parser.add_argument("--image", help="Input image URL (keyframe 首帧, reference 图片, or simple image-to-video)")
    vid_parser.add_argument("--first-frame", help="Keyframe mode: first frame image URL")
    vid_parser.add_argument("--last-frame", help="Keyframe mode: last frame image URL")
    vid_parser.add_argument("--images", help="Reference mode: comma-separated image URLs")
    vid_parser.add_argument("--audios", help="Reference mode: comma-separated audio URLs (Flash <=3)")
    vid_parser.add_argument("--negative-prompt", help="Negative prompt")
    vid_parser.add_argument("--poll", action="store_true", help="Poll for result automatically")
    vid_parser.add_argument("--max-wait", type=int, default=600, help="Max polling time in seconds (default: 600)")
    vid_parser.add_argument("--poll-interval", type=int, default=5, help="Polling interval in seconds (default: 5)")
    vid_parser.add_argument("--output-dir", default=".", help="Directory to save output files")

    # Video query command
    q_parser = sub.add_parser("video-query", help="Query video result by video_id")
    q_parser.add_argument("--video-id", required=True, help="Video ID to query")
    q_parser.add_argument("--output-dir", default=".", help="Directory to save output files")

    args = parser.parse_args()

    # 根据命令行 / 环境变量确定最终站点、模型
    global API_BASE, VIDEO_QUERY_BASE, IMAGE_MODEL, VIDEO_MODEL
    API_BASE = args.api_base or resolve_api_base()
    VIDEO_QUERY_BASE = resolve_query_base(API_BASE)
    IMAGE_MODEL = os.environ.get("AGNES_IMAGE_MODEL") or IMAGE_MODEL_DEFAULT
    VIDEO_MODEL = os.environ.get("AGNES_VIDEO_MODEL") or VIDEO_MODEL_DEFAULT

    if args.command == "image":
        generate_image(args)
    elif args.command == "video":
        generate_video(args)
    elif args.command == "video-query":
        query_video(args)


if __name__ == "__main__":
    main()
