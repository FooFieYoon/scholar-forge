---
name: agnes-image-video
description: "Agnes AI 图片生成和视频生成能力。支持文生图、图生图、文生视频、图生视频。当用户请求生成图片、生成视频、AI绘图、AI视频、制作图片、制作视频时触发此技能。"
---

# Agnes AI 图片 & 视频生成

通过 Agnes AI API 生成高质量图片和视频。API 兼容 OpenAI 格式，使用 Bearer Token 认证。

> **模型版本（2026-09 更新）**：图片使用 **`agnes-image-2.5-flash`**，视频使用 **`agnes-video-2.5-flash`**（限时免费，固定 720P）。原 `agnes-video-v2.0` 已于 2026-09-25 正式下线，请勿再调用。
>
> **API 站点可切换（中国站 / 国际站均可）**：脚本默认使用国际站 `https://apihub.agnes-ai.com/v1`。若你的 API Key 属于中国站，请在 `<SKILL_DIR>/.env` 增加一行 `AGNES_API_BASE=https://api.agnes-ai.cn/v1`（别名 `AGNES_BASE_URL` 亦可），脚本会自动适配对应的视频查询域名；也可在命令行加 `--api-base https://api.agnes-ai.cn/v1`。**无需修改任何代码**，两种站点都能正常运行。

## 前置条件

- API Key 已配置在 `<SKILL_DIR>/.env`（首次使用时请更新）
- 可选：在 `.env` 设置 `AGNES_API_BASE`（中国站 `https://api.agnes-ai.cn/v1` / 国际站 `https://apihub.agnes-ai.com/v1`，默认国际站）；不设置则使用默认国际站
- 脚本位置：`<SKILL_DIR>/scripts/agnes-ai.py`

**Windows 路径**：
```
C:/Users/<user>/AppData/Local/Programs/WorkBuddy/resources/app.asar.unpacked/resources/builtin-skills/agnes-image-video/scripts/agnes-ai.py
```

## 图像生成

当前使用 **`agnes-image-2.5-flash`**（免费，支持文生图、图生图、多图合成）。

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

视频生成是**异步**的：先创建任务，再轮询结果。当前使用 **`agnes-video-2.5-flash`**（限时免费，固定 720P，支持 `text` / `keyframe` / `reference` 三种模式）。原 `agnes-video-v2.0` 已于 2026-09-25 下线，请勿再使用。

### 文生视频

```bash
# 提交任务（不等待）
python <SKILL_DIR>/scripts/agnes-ai.py video \
  --prompt "A cinematic shot of a cat walking on the beach at sunset" \
  --seconds 5 --size 720P --aspect-ratio 16:9

# 自动轮询等待结果（推荐）
python <SKILL_DIR>/scripts/agnes-ai.py video \
  --prompt "..." --seconds 5 --size 720P --aspect-ratio 16:9 \
  --poll --max-wait 600
```

### 图生视频（keyframe 首帧）

```bash
python <SKILL_DIR>/scripts/agnes-ai.py video \
  --prompt "Person slowly turns around and looks at the camera" \
  --image "https://example.com/photo.jpg" \
  --mode keyframe --poll
```

### 首尾帧控制（keyframe）

```bash
python <SKILL_DIR>/scripts/agnes-ai.py video \
  --prompt "..." --mode keyframe \
  --first-frame "https://example.com/first.png" \
  --last-frame "https://example.com/last.png" --poll
```

### 图片/音频参考（reference）

```bash
python <SKILL_DIR>/scripts/agnes-ai.py video \
  --prompt "以 <Picture 1> 的角色风格为参考，角色在花田中奔跑" \
  --mode reference --images "https://example.com/char.png" --poll
```

参数：
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--prompt` | 视频描述（必填） | — |
| `--mode` | 生成模式：`text` / `keyframe` / `reference` | `text` |
| `--seconds` | 视频时长（字符串 `"4"`–`"12"`） | `5` |
| `--size` | 分辨率档位：`720P`（Flash 仅支持 720P）/ `1080P` / `1K` / `2K` | `720P` |
| `--aspect-ratio` | 画幅：`16:9`/`9:16`/`1:1`/`4:3`/`3:4`/`21:9` | `16:9` |
| `--seed` | 随机种子（可复现） | — |
| `--image` | 输入图片 URL（keyframe 首帧 / reference 图片 / 简单图生视频） | — |
| `--first-frame` | keyframe 模式首帧图片 URL | — |
| `--last-frame` | keyframe 模式尾帧图片 URL | — |
| `--images` | reference 模式逗号分隔图片 URL 列表（Flash ≤5 张） | — |
| `--audios` | reference 模式逗号分隔音频 URL 列表（Flash ≤3 段） | — |
| `--negative-prompt` | 反向提示词 | — |
| `--poll` | 自动轮询等待结果 | 不等待 |
| `--max-wait` | 最大等待秒数 | 600 |
| `--output-dir` | 输出目录 | `.` |

模式说明：
- `text`：纯文生视频（可单独传 `--image` 自动转为 keyframe 首帧）。
- `keyframe`：用首帧 / 尾帧 / 首尾帧控制起止构图，至少提供 `--first-frame` 或 `--last-frame` 之一。
- `reference`：用图片 / 音频作为风格或内容参考，传入 `--images` 或 `--audios`。

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
