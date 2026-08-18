# Agnes AI Video API Reference

## Model
`agnes-video-v2.0`

## Endpoints
- Create: `POST https://apihub.agnes-ai.com/v1/videos`
- Query (recommended): `GET https://apihub.agnes-ai.com/agnesapi?video_id=<VIDEO_ID>`
- Query (legacy): `GET https://apihub.agnes-ai.com/v1/videos/<TASK_ID>`

## Headers
```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

## Create Task Parameters

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | `agnes-video-v2.0` |
| `prompt` | string | ✅ | 视频内容描述 |
| `image` | string | ❌ | 图生视频输入图片 URL |
| `mode` | string | ❌ | 生成模式：`ti2vid` 或 `keyframes` |
| `height` | integer | ❌ | 视频高度，默认 768 |
| `width` | integer | ❌ | 视频宽度，默认 1152 |
| `num_frames` | integer | ❌ | 帧数，≤441 且遵循 8n+1 规则 |
| `frame_rate` | number | ❌ | 帧率，1-60 |
| `negative_prompt` | string | ❌ | 反向提示词 |
| `extra_body.image` | array | ❌ | 关键帧模式输入图片 URL 数组 |
| `extra_body.mode` | string | ❌ | 附加模式设置，如 `keyframes` |

## Response (Create)
```json
{
  "id": "task_xxx",
  "task_id": "task_xxx",
  "video_id": "video_xxx",
  "object": "video",
  "model": "agnes-video-v2.0",
  "status": "queued",
  "progress": 0,
  "created_at": 1780457477,
  "seconds": "10.0",
  "size": "1280x768"
}
```

## Response (Query - Completed)
```json
{
  "id": "task_xxx",
  "video_id": "video_xxx",
  "task_id": "task_xxx",
  "object": "video",
  "model": "agnes-video-v2.0",
  "status": "completed",
  "progress": 100,
  "created_at": 1780457477,
  "completed_at": 1784530510,
  "seconds": "10.0",
  "size": "1280x768",
  "metadata": {
    "size_mapping": {
      "adjusted": true,
      "height": 768,
      "ratio": "16:9",
      "resolution": "720p",
      "width": 1280
    },
    "url": "https://platform-outputs.agnes-ai.space/videos/agnes-video-v2.0/task_xxx.mp4"
  }
}
```

## Task Status
| 状态 | 说明 |
|------|------|
| `queued` | 等待生成 |
| `in_progress` | 生成中 |
| `completed` | 生成完成 |
| `failed` | 生成失败 |

## Duration Control
- `seconds = num_frames / frame_rate`
- 常用参数：
  - 约 3 秒：`num_frames: 81`, `frame_rate: 24`
  - 约 5 秒：`num_frames: 121`, `frame_rate: 24`
  - 约 10 秒：`num_frames: 241`, `frame_rate: 24`
  - 约 18 秒：`num_frames: 441`, `frame_rate: 24`

## Resolution Presets
- 480p, 720p, 1080p（系统自动标准化）
- 推荐宽高比：16:9（横版）、9:16（竖版）、1:1（方形）

## Pricing
- 视频时长：当前免费（$0/秒）

## Documentation
- Video API: https://agnes-ai.com/zh-Hans/docs/agnes-video-v20
- Overview: https://agnes-ai.cn/zh-Hans/docs/overview
