# Agnes AI Image API Reference

## Model
`agnes-image-2.1-flash`

## Endpoint
`POST https://apihub.agnes-ai.com/v1/images/generations`

## Headers
```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

## Request Body

### 基础参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | `agnes-image-2.1-flash` |
| `prompt` | string | ✅ | 图像生成/编辑的文字指令 |
| `size` | string | ✅ | 输出尺寸：`1K`/`2K`/`3K`/`4K` 或精确如 `1024x768` |
| `ratio` | string | ❌ | 宽高比：`1:1`/`3:4`/`4:3`/`16:9`/`9:16`/`2:3`/`3:2`/`21:9`，默认 `1:1` |

### 高级参数 (extra_body)
| 参数 | 类型 | 说明 |
|------|------|------|
| `extra_body.image` | string[] | 输入图片数组（图生图/多图合成时必填），支持 HTTPS URL 或 Data URI Base64 |
| `extra_body.response_format` | string | 输出格式：`url` 或 `b64_json` |

### 文生图专用
| 参数 | 类型 | 说明 |
|------|------|------|
| `return_base64` | boolean | 设为 true 时输出 Base64 格式 |

## Response

### URL 输出
```json
{
  "created": 1780000000,
  "data": [
    {
      "url": "https://storage.googleapis.com/agnes-aigc/xxx.png",
      "b64_json": null,
      "revised_prompt": null
    }
  ]
}
```

### Base64 输出
```json
{
  "created": 1780000000,
  "data": [
    {
      "url": null,
      "b64_json": "iVBORw0KGgo...",
      "revised_prompt": null
    }
  ]
}
```

## Size/Ratio Mapping

| Ratio | 1K | 2K | 3K | 4K |
|-------|----|----|----|----|
| 1:1 | 1024×1024 | 2048×2048 | 3072×3072 | 4096×4096 |
| 3:4 | 864×1152 | 1728×2304 | 2592×3456 | 3456×4608 |
| 4:3 | 1152×864 | 2304×1728 | 3456×2592 | 4608×3456 |
| 16:9 | 1312×736 | 2624×1472 | 3936×2208 | 5248×2944 |
| 9:16 | 736×1312 | 1472×2624 | 2208×3936 | 2944×5248 |
| 2:3 | 832×1248 | 1664×2496 | 2496×3744 | 3328×4992 |
| 3:2 | 1248×832 | 2496×1664 | 3744×2496 | 4992×3328 |
| 21:9 | 1568×672 | 3136×1344 | 4704×2016 | 6272×2688 |

## Common Errors
| 问题 | 正确做法 |
|------|----------|
| response_format 放在顶层 | 放入 `extra_body.response_format` |
| 图生图缺少图片参数 | 通过 `extra_body.image` 提供 |
| 输入图片 URL 无法访问 | 使用公开 HTTPS URL 或 Data URI |
| 请求超时 | 设置超时 60s-360s |

## Documentation
- Image API: https://agnes-ai.com/doc/agnes-image-21-flash
- Overview: https://agnes-ai.cn/zh-Hans/docs/overview
