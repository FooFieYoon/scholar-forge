# Agnes AI Video API Reference

## Model
`agnes-video-2.5-flash`

> 限时免费（原价 $0.025/秒，现 $0/秒），固定 720P。复用 Agnes Video 2.5 的模型能力与异步任务接口。
> 原 `agnes-video-v2.0` 已于 2026-09-25 23:59:59（UTC+8）正式下线，请勿再调用。

## Endpoints
- Create: `POST https://apihub.agnes-ai.com/v1/videos`
- Query (recommended): `GET https://apihub.agnes-ai.com/agnesapi?video_id=<VIDEO_ID>&model_name=agnes-video-2.5-flash`
- Query (legacy, 仅 text 模式): `GET https://apihub.agnes-ai.com/agnesapi?video_id=<VIDEO_ID>`

> 2.5 系列所有模式均推荐在查询 URL 中携带 `model_name=agnes-video-2.5-flash`；`keyframe` / `reference` 模式必须携带，否则查询会失败。

## Headers
```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

## Create Task Parameters

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | `agnes-video-2.5-flash` |
| `prompt` | string | ✅ | 视频内容描述。reference 模式可用 `<Picture N>` / `<Audio N>` 指代素材 |
| `mode` | string | ✅ | 生成模式：`text` / `keyframe` / `reference` |
| `seconds` | string | ❌ | 视频时长，字符串 `"4"`–`"12"`，默认 `"5"` |
| `size` | string | ❌ | 分辨率档位。Flash 固定 `"720P"`；其他值返回 HTTP 400 |
| `aspect_ratio` | string | ❌ | 画幅比例，默认 `16:9` |
| `seed` | integer | ❌ | 随机种子，相同种子可提高可复现性 |
| `n` | integer | ❌ | 生成数量，当前仅支持 `1` |

### 模式专用参数
| 参数 | 类型 | 适用模式 | 说明 |
|------|------|----------|------|
| `first_frame` | string | keyframe | 首帧图片 URL，与 `last_frame` 至少提供一个 |
| `last_frame` | string | keyframe | 尾帧图片 URL，与 `first_frame` 至少提供一个 |
| `images` | string[] | reference | 参考图片 URL 列表，Flash 最多 5 张 |
| `audios` | string[] | reference | 参考音频 URL 列表，Flash 最多 3 段 |
| `videos` | object[] | reference | 参考视频列表；**Flash 不支持**，传入有效内容返回 HTTP 400 |

所有媒体 URL 必须可由 Agnes AI 服务公开访问。

## Response (Create)
```json
{
  "id": "task_xxx",
  "task_id": "task_xxx",
  "video_id": "video_xxx",
  "object": "video",
  "model": "agnes-video-2.5-flash",
  "status": "queued",
  "progress": 0,
  "created_at": 1780457477,
  "seconds": "5",
  "size": "720P"
}
```

## Response (Query - Completed)
```json
{
  "id": "task_xxx",
  "video_id": "video_xxx",
  "task_id": "task_xxx",
  "object": "video",
  "model": "agnes-video-2.5-flash",
  "status": "completed",
  "progress": 100,
  "created_at": 1780457477,
  "completed_at": 1784530510,
  "seconds": "5",
  "size": "720P",
  "url": "https://example.com/generated/video.mp4"
}
```

> 2.5 系列视频地址位于响应**顶层 `url` 字段**（不再是 v2.0 的 `metadata.url`）。

## Task Status
| 状态 | 说明 |
|------|------|
| `queued` | 等待生成 |
| `in_progress` | 生成中 |
| `completed` | 生成完成，读取顶层 `url` |
| `failed` | 生成失败，见 `error.message` |

## Resolution & Aspect Ratio (Flash 720P)
| aspect_ratio | 输出像素 |
|--------------|----------|
| 21:9 | 1680×720 |
| 16:9 | 1280×704 |
| 4:3 | 960×720 |
| 1:1 | 720×720 |
| 3:4 | 720×960 |
| 9:16 | 720×1280 |

## Flash 限制（校验失败返回 HTTP 400）
- `size` 非 `720P` → `size must be 720P`
- `images` 超过 5 张 → `images length must not exceed 5`
- `audios` 超过 3 段 → `audios length must not exceed 3`
- 传入有效 `videos` → `videos is not supported`

## Pricing
- 2.5 Flash：当前限时免费（$0/秒）。免费政策如有调整以 Agnes AI 平台公告为准。
- 2.5（非 Flash）：720P $0.025/秒、1080P 与 1K $0.040/秒、2K $0.055/秒。

## Documentation
- Video 2.5 Flash: https://agnes-ai.com/zh-Hans/docs/agnes-video-25-flash
- Video 2.5: https://agnes-ai.com/zh-Hans/docs/agnes-video-25
- Overview: https://agnes-ai.cn/zh-Hans/docs/overview
