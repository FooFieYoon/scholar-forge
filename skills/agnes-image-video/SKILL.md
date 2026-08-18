---
name: agnes-image-video
description: "Agnes AI 图片生成和视频生成能力。支持文生图、图生图、文生视频、图生视频。当用户请求生成图片、生成视频、AI绘图、AI视频、制作图片、制作视频时触发此技能。"
---

# Agnes AI 图片 & 视频生成

通过 Agnes AI API 生成高质量图片和视频。API 兼容 OpenAI 格式，使用 Bearer Token 认证。

## 前置条件

- API Key 已配置在 `<SKILL_DIR>/.env`（首次使用时请更新）
- 脚本位置：`<SKILL_DIR>/scripts/agnes-ai.py`

**Windows 路径**：
```
C:/Users/<user>/AppData/Local/Programs/WorkBuddy/resources/app.asar.unpacked/resources/builtin-skills/agnes-image-video/scripts/agnes-ai.py
```

## 图像生成

### 文生图

```bash
python <SKILL_DIR>/scripts/agnes-ai.py image \
  --prompt "A luminous floating city above a misty canyon at sunrise, cinematic realism" \
  --size 2K --ratio 16:9
```

参数：
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--prompt` | 文本描述（必填） | — |
| `--size` | 尺寸：1K/2K/3K/4K 或精确值如 `1024x768` | `1K` |
| `--ratio` | 宽高比：`1:1`/`16:9`/`9:16`/`4:3`/`3:4`/`2:3`/`3:2`/`21:9` | `1:1` |
| `--output-format` | `url` 或 `b64` | `url` |
| `--output-dir` | 输出目录 | `.` |

常用尺寸：
| 尺寸 | 1K | 2K | 3K | 4K |
|------|-----|-----|-----|-----|
| 16:9 | 1312×736 | 2624×1472 | 3936×2208 | 5248×2944 |
| 9:16 | 736×1312 | 1472×2624 | 2208×3936 | 2944×5248 |
| 1:1 | 1024×1024 | 2048×2048 | 3072×3072 | 4096×4096 |

### 图生图

```bash
python <SKILL_DIR>/scripts/agnes-ai.py image \
  --prompt "Transform into a cyberpunk neon style" \
  --image "https://example.com/input.jpg" \
  --size 1024x768
```

## 视频生成

视频生成是**异步**的：先创建任务，再轮询结果。

### 文生视频

```bash
# 提交任务（不等待）
python <SKILL_DIR>/scripts/agnes-ai.py video \
  --prompt "A cinematic shot of a cat walking on the beach at sunset" \
  --width 1152 --height 768 --num-frames 121 --frame-rate 24

# 自动轮询等待结果（推荐）
python <SKILL_DIR>/scripts/agnes-ai.py video \
  --prompt "..." \
  --width 1152 --height 768 --num-frames 121 --frame-rate 24 \
  --poll --max-wait 600
```

### 图生视频

```bash
python <SKILL_DIR>/scripts/agnes-ai.py video \
  --prompt "Person slowly turns around and looks at the camera" \
  --image "https://example.com/photo.jpg" \
  --poll
```

参数：
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--prompt` | 视频描述（必填） | — |
| `--image` | 输入图片 URL（图生视频） | — |
| `--keyframe-images` | 逗号分隔的关键帧 URL 列表 | — |
| `--width` | 视频宽度 | 1152 |
| `--height` | 视频高度 | 768 |
| `--num-frames` | 帧数（≤441，遵循 8n+1） | — |
| `--frame-rate` | 帧率（1-60） | 24 |
| `--negative-prompt` | 反向提示词 | — |
| `--poll` | 自动轮询等待结果 | 不等待 |
| `--max-wait` | 最大等待秒数 | 600 |
| `--output-dir` | 输出目录 | `.` |

帧数规则：必须 ≤ 441 且满足 `8n+1`，常用值：81（约3秒）、121（约5秒）、241（约10秒）、441（约18秒）。

### 查询视频结果

```bash
python <SKILL_DIR>/scripts/agnes-ai.py video-query --video-id "video_xxxxx"
```

## Agent 执行规范

1. **认证**：从 `<SKILL_DIR>/.env` 自动加载 API Key，禁止在命令行中暴露 Key
2. **输出下载**：API 返回的 URL 必须下载到本地后再展示给用户（脚本已内置此逻辑）
3. **视频异步**：视频生成耗时 1~5 分钟，使用 `--poll` 自动等待，无需手动 sleep 重试
4. **禁止伪造**：失败时直接报告错误，不得编造结果
5. **路径**：Windows 下脚本路径使用正斜杠，优先使用 Bash 工具执行
6. **Python 版本**：使用系统 Python 3.7+（脚本仅依赖标准库，无需额外安装）

## 示例用法

```bash
# 生成一张 2K 横版风景图
python scripts/agnes-ai.py image --prompt "Mountains at golden hour, epic landscape photography" --size 2K --ratio 16:9

# 生成一个 5 秒短视频（自动轮询）
python scripts/agnes-ai.py video --prompt "Ocean waves crashing on rocky shore, slow motion" --poll

# 查询已提交的任务
python scripts/agnes-ai.py video-query --video-id "video_abc123"
```
