---
name: sensenova-image
description: 使用商汤日日新 SenseNova U1 Fast 模型生成图片（文生图，2K 高分辨率，擅长信息图/海报/图表）。当用户要求用日日新/SenseNova/U1 生图，或需要生成中文信息图、知识图解、海报、图表类图片时触发。注意 U1 Fast 是纯生图模型，不能作为对话模型使用。
agent_created: true
---

# SenseNova U1 Fast 图像生成

商汤日日新 `sensenova-u1-fast` 是**纯图像生成模型**，只能通过 `/v1/images/generations` 端点调用。
它 **不能** 配置进 `models.json` 当对话模型用——那样请求 `/v1/chat/completions` 会返回 `model is not found`。

## 快速调用

```bash
C:/Users/foofi/.workbuddy/binaries/python/envs/default/Scripts/python.exe \
  C:/Users/foofi/.workbuddy/skills/sensenova-image/scripts/gen_image.py \
  --prompt "提示词" --size 2048x2048 --out ./generated-images
```

参数：
- `--prompt` 必填，提示词。中文效果好，适合信息图/图表/海报。
- `--size` 可选，默认 `2048x2048`。**必须**是下方合法值之一。
- `--n` 可选，默认 1。
- `--out` 可选，输出目录，默认 `./generated-images`。
- `--no-watermark` 可选，关闭水印。

## 合法尺寸（实测，13 种，其它值一律 400）

| 比例 | 尺寸 |
|---|---|
| 竖版 2:3 | `1664x2496` |
| 横版 3:2 | `2496x1664` |
| 竖版 3:4 | `1760x2368` |
| 横版 4:3 | `2368x1760` |
| 竖版 4:5 | `1824x2272` |
| 横版 5:4 | `2272x1824` |
| 方形 1:1 | `2048x2048` |
| 横版 16:9 | `2752x1536` |
| 竖版 9:16 | `1536x2752` |
| 超宽 | `3072x1376` |
| 超高 | `1344x3136` |
| 长条横幅 | `2560x720` |
| 长条横幅大 | `3072x864` |

常见错误：传 `1024x1024`、`1920x1080` 会直接报 `field Size invalid`。

## 接口原始形态

```
POST https://token.sensenova.cn/v1/images/generations
Authorization: Bearer sk-B7flAfr3sCoFSY8U8HPscmF9pPQNC3of
{"model":"sensenova-u1-fast","prompt":"...","n":1,"size":"2048x2048","watermark":true}
```

返回 `data[].url`，**URL 有效期约 24 小时**，必须立即下载到本地再交付给用户。

## 限流处理

免费额度 RPM 很低。收到 429（`rpm exhausted` / `quota_exceeded_error` / `insufficient_quota`）时**指数退避重试**，脚本已内置 5 次重试。不要并发批量出图。

## 交付

出图后用 `present_files` 展示本地 png 路径，不要只给远程 URL。
