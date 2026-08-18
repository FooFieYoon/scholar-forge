#!/usr/bin/env python3
"""
Agnes AI Image & Video Generation Script

Usage:
    # Image generation
    python agnes-ai.py image --prompt "a cute cat" --size 1K --ratio 16:9 --output-dir ./output

    # Image generation (Base64)
    python agnes-ai.py image --prompt "a cute cat" --size 1K --ratio 16:9 --output-format b64

    # Video generation (text-to-video)
    python agnes-ai.py video --prompt "a cat walking on the beach" --width 1152 --height 768 --num-frames 121 --frame-rate 24

    # Video generation (image-to-video)
    python agnes-ai.py video --prompt "person turns around" --image "https://example.com/image.jpg"

    # Video result query
    python agnes-ai.py video-query --video-id "video_xxx"

    # Polling video (auto-wait)
    python agnes-ai.py video --prompt "..." --poll --max-wait 600

API Reference: https://agnes-ai.com/doc/agnes-image-21-flash
              https://agnes-ai.com/zh-Hans/docs/agnes-video-v20
"""

import argparse
import base64
import json
import os
import sys
import time

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
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path


API_BASE = "https://api.agnes-ai.cn/v1"
VIDEO_QUERY_BASE = "https://api.agnes-ai.cn/agnesapi"


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
    """Generate image using agnes-image-2.1-flash."""
    api_key = get_api_key()

    body = {
        "model": "agnes-image-2.1-flash",
        "prompt": args.prompt,
        "size": args.size,
    }

    if hasattr(args, "ratio") and args.ratio:
        body["ratio"] = args.ratio

    if hasattr(args, "image") and args.image:
        body["extra_body"] = {"image": [args.image]}
        if hasattr(args, "output_format") and args.output_format == "b64":
            body["extra_body"]["response_format"] = "b64_json"
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
    """Generate video using agnes-video-v2.0 (async)."""
    api_key = get_api_key()

    body = {
        "model": "agnes-video-v2.0",
        "prompt": args.prompt,
    }

    if hasattr(args, "image") and args.image:
        body["image"] = args.image

    if hasattr(args, "width") and args.width:
        body["width"] = args.width
    if hasattr(args, "height") and args.height:
        body["height"] = args.height
    if hasattr(args, "num_frames") and args.num_frames:
        body["num_frames"] = args.num_frames
    if hasattr(args, "frame_rate") and args.frame_rate:
        body["frame_rate"] = args.frame_rate

    if hasattr(args, "mode") and args.mode:
        body["mode"] = args.mode

    if hasattr(args, "negative_prompt") and args.negative_prompt:
        body["negative_prompt"] = args.negative_prompt

    if hasattr(args, "keyframe_images") and args.keyframe_images:
        body["extra_body"] = {
            "image": args.keyframe_images.split(","),
            "mode": "keyframes"
        }

    result = api_request("videos", body=body, api_key=api_key)

    if "video_id" not in result:
        print(json.dumps({"error": "NO_VIDEO_ID", "response": result}))
        return

    video_id = result["video_id"]
    task_id = result.get("task_id", video_id)

    if hasattr(args, "poll") and args.poll:
        max_wait = getattr(args, "max_wait", 600)
        poll_interval = getattr(args, "poll_interval", 10)
        _poll_video(video_id, task_id, max_wait, poll_interval, args)
    else:
        print(json.dumps({
            "status": "submitted",
            "video_id": video_id,
            "task_id": task_id,
            "message": "Video generation task submitted. Use --video-id to poll for results."
        }))


def _poll_video(video_id, task_id, max_wait, poll_interval, args):
    """Poll for video result until completion or timeout."""
    api_key = get_api_key()
    start = time.time()
    output_dir = Path(args.output_dir) if hasattr(args, "output_dir") and args.output_dir else Path(".")
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    while time.time() - start < max_wait:
        # Try the recommended query endpoint
        url = f"{VIDEO_QUERY_BASE}?video_id={video_id}"
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
            video_url = (result.get("metadata", {}) or {}).get("url") or result.get("url")
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

    url = f"{VIDEO_QUERY_BASE}?video_id={video_id}"
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
        video_url = result.get("metadata", {}).get("url")
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
    parser = argparse.ArgumentParser(description="Agnes AI Image & Video Generation CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    # Image command
    img_parser = sub.add_parser("image", help="Generate image from text")
    img_parser.add_argument("--prompt", required=True, help="Text prompt for image generation")
    img_parser.add_argument("--size", default="1K",
                            help="Output size: 1K, 2K, 3K, 4K, or custom like 1024x768 (default: 1K)")
    img_parser.add_argument("--ratio", default="1:1",
                            help="Aspect ratio: 1:1, 16:9, 9:16, 4:3, 3:4, 2:3, 3:2, 21:9 (default: 1:1)")
    img_parser.add_argument("--image", help="Input image URL for image-to-image")
    img_parser.add_argument("--output-format", choices=["url", "b64"], default="url",
                            help="Output format: url (default) or b64 (base64)")
    img_parser.add_argument("--output-dir", default=".", help="Directory to save output files")

    # Video command
    vid_parser = sub.add_parser("video", help="Generate video from text or image")
    vid_parser.add_argument("--prompt", required=True, help="Text prompt for video generation")
    vid_parser.add_argument("--image", help="Input image URL for image-to-video")
    vid_parser.add_argument("--keyframe-images", help="Comma-separated list of keyframe image URLs")
    vid_parser.add_argument("--width", type=int, help="Video width (default: 1152)")
    vid_parser.add_argument("--height", type=int, help="Video height (default: 768)")
    vid_parser.add_argument("--num-frames", type=int, help="Number of frames (must be <= 441, follow 8n+1 rule)")
    vid_parser.add_argument("--frame-rate", type=float, help="Frame rate (default: 24)")
    vid_parser.add_argument("--mode", help="Generation mode: ti2vid, keyframes")
    vid_parser.add_argument("--negative-prompt", help="Negative prompt")
    vid_parser.add_argument("--poll", action="store_true", help="Poll for result automatically")
    vid_parser.add_argument("--max-wait", type=int, default=600, help="Max polling time in seconds (default: 600)")
    vid_parser.add_argument("--poll-interval", type=int, default=10, help="Polling interval in seconds (default: 10)")
    vid_parser.add_argument("--output-dir", default=".", help="Directory to save output files")

    # Video query command
    q_parser = sub.add_parser("video-query", help="Query video result by video_id")
    q_parser.add_argument("--video-id", required=True, help="Video ID to query")
    q_parser.add_argument("--output-dir", default=".", help="Directory to save output files")

    args = parser.parse_args()

    if args.command == "image":
        generate_image(args)
    elif args.command == "video":
        generate_video(args)
    elif args.command == "video-query":
        query_video(args)


if __name__ == "__main__":
    main()
