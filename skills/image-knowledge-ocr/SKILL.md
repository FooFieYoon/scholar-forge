---
name: image-knowledge-ocr
description: 从图片文件夹中批量提取文字（OCR）、按内容分类整理知识、上传至IMA知识库的全流程自动化技能。适用于：1）处理手机截图/照片中的知识内容；2）批量OCR识别图片文字；3）将OCR结果分类整理为知识笔记；4）上传笔记至IMA"日常"知识库。触发词：整理图片知识、图片OCR、截图整理、知识提取、IMA上传。
agent_created: true
---

# 图片知识OCR提取与IMA上传

## 概述

本技能提供从图片文件夹中批量提取知识内容并上传至IMA知识库的完整工作流。涵盖HEIC/JPG/PNG/WEBP等格式，使用RapidOCR进行中文OCR识别，multiprocessing加速处理，最后按9大知识类别分类并创建详细笔记。

## 前置条件

- Python 3.13+（使用隔离venv）
- Node.js 22+
- 安装依赖：`pip install rapidocr-onnxruntime pillow-heif`
- IMA凭证文件：`~/.config/ima/client_id` 和 `api_key`（需清除UTF-8 BOM）
- IMA OpenAPI调用需设置环境变量：`IMA_FORCE_UPDATE_CHECK=1`

## 工作流程

### 第1步：准备OCR脚本

使用以下脚本处理图片文件夹：

```bash
# 关键配置
IMAGE_DIR="图片文件夹的绝对路径"
OUTPUT_FILE="ocr_results.txt"
NUM_WORKERS=4  # 根据CPU核心数调整
CONFIDENCE_THRESHOLD=0.3
```

### 第2步：执行OCR识别

脚本特性：
- **多进程处理**：`multiprocessing.Pool` + `initializer`，每个worker独立加载模型
- **增量写入**：实时输出到 `ocr_results.txt`，可监控进度
- **断点续跑**：跳过已处理图片，支持中断后继续
- **HEIC支持**：`pillow-heif` 读取iPhone HEIC格式
- **置信度过滤**：跳过置信度低于阈值的图片

输出格式：
```
## IMG_1234.HEIC
（OCR识别的文字内容，每行一段）

## IMG_5678.JPG
（文字内容）
```

### 第3步：读取并分析OCR结果

读取完整 `ocr_results.txt`，按以下9个类别整理知识内容：

1. **AI与大模型工具生态**
   - 大模型API服务（免费/付费）
   - AI编程助手、Skills
   - AIGC工具（文生图、文生视频、3D模型）
   - Context Engineering vs Prompt Engineering

2. **AI编程Skills与工作流**
   - academic-skills（学术研究10个子技能）
   - drawio-skill、tldraw-skill
   - html-ppt-skill、jianying-Skill
   - CocoLoop、TRAE SOLO、Hermes Agent、OpenClaw多agent

3. **开源项目与工具收藏**
   - MoneyPrinterTurbo（视频生成52K stars）
   - coding-interview-university（340K stars）
   - buildyourownx系列
   - Obsidian+OpenCode、SoloMD

4. **科研学术资源**
   - AI学术工作流（vibe research）
   - Veusz科学绘图
   - research框架、paper2any
   - 科研绘图（Gemini+Nano Banana+Vectorizer）

5. **毕业论文与学术诚信**
   - 代写风险警示、论文查重规则
   - 论文生成skill
   - 答辩时间节点、查重规则（维普20%/AI 30%）

6. **编程开发笔记**
   - 文件搜索工具（Everything/Listary/AnyText）
   - Godot游戏引擎
   - VBA代码生成PPT、Check_Device_by_WiFi

7. **职场维权与法律**
   - 7要3不签原则
   - 维权渠道（12315/黑猫/领导留言板/12348/12345/12366）
   - 辞职信模板

8. **网络资源与生活技巧**
   - KMS.CX Windows激活
   - 湖北省图书馆知网免费入口
   - 美式证件照ChatGPT prompt、春节红包攻略

9. **3D设计与视频制作**
   - Autodesk Fusion AI
   - 有言3D数字人
   - Pixelle-Video、YangAgent skill自动化

### 第4步：创建详细笔记

使用 `openapi/note/v1/import_doc` API 创建9篇详细笔记：

**API调用格式：**
```bash
IMA_FORCE_UPDATE_CHECK=1 node "$SKILL_DIR/../ima-skills/ima_api.cjs" \
  "openapi/note/v1/import_doc" '{
    "title": "笔记标题",
    "content": "# Markdown内容（3000-5000字）",
    "content_format": 1
  }'
```

**关键参数：**
- `content_format`: 1 = MARKDOWN（不是"markdown"字符串）
- 每篇笔记3000-5000字，包含工具名称、URL、详细步骤、案例等
- API返回 `note_id`，需记录用于后续添加到知识库

**重要：note_id不一致问题**
- API返回的 `note_id` 与实际保存的笔记ID不同
- 必须通过 `openapi/note/v1/list_note` 获取正确的note_id：
  ```bash
  IMA_FORCE_UPDATE_CHECK=1 node ima_api.cjs "openapi/note/v1/list_note" '{
    "folder_id": "",
    "cursor": "",
    "limit": 100
  }'
  ```
- 返回结果中的 `note_id` 才是 `add_knowledge` 需要的值

### 第5步：添加笔记到知识库

使用 `openapi/wiki/v1/add_knowledge` API：

**API调用格式：**
```bash
IMA_FORCE_UPDATE_CHECK=1 node "$SKILL_DIR/../ima-skills/ima_api.cjs" \
  "openapi/wiki/v1/add_knowledge" '{
    "media_type": 11,
    "note_info": {
      "content_id": "<正确获取的note_id>"
    },
    "title": "笔记标题",
    "knowledge_base_id": "<base64格式的知识库ID>"
  }'
```

**关键参数说明：**
- `media_type`: 11 = 笔记
- `note_info.content_id`: 第4步获取的正确note_id
- `knowledge_base_id`: 使用 **base64格式**（不是数字ID）
- `title`: 笔记标题（可选，但建议提供）

**知识库ID获取：**
- MCP工具返回数字ID（如 `7469983902738366`）
- Wiki API需要base64格式（如 `InvlbvCKbDPjQTRorNwt87cC8p7EPmpGbHulGb3pWlc=`）
- 通过 `search_knowledge` 获取base64格式：
  ```bash
  IMA_FORCE_UPDATE_CHECK=1 node ima_api.cjs "openapi/wiki/v1/search_knowledge" '{
    "page": {"page_num": 1, "page_size": 20},
    "keyword": "日常"
  }'
  ```

### 第6步：验证上传结果

```bash
# 验证笔记内容
IMA_FORCE_UPDATE_CHECK=1 node ima_api.cjs "openapi/note/v1/get_doc_content" '{
  "note_id": "<note_id>",
  "target_content_format": 0
}'

# 验证知识库状态
IMA_FORCE_UPDATE_CHECK=1 node ima_api.cjs "openapi/wiki/v1/search_knowledge" '{
  "page": {"page_num": 1, "page_size": 20},
  "knowledge_base_id": "<base64_kb_id>"
}'
```

## 常见问题与解决方案

### 1. IMA API认证失败
- **问题**：`auth` 或 `version check` 相关错误
- **解决**：
  - 清除 `~/.config/ima/client_id` 和 `api_key` 文件的UTF-8 BOM
  - 首次调用设置 `IMA_FORCE_UPDATE_CHECK=1` 环境变量

### 2. 知识库添加失败
- **问题**：`invalid knowledge_base_id` 或 `invalid KnowledgeBaseId`
- **解决**：
  - 必须使用base64格式ID，不是数字ID
  - `note_info` 格式必须是 `{ "content_id": "<note_id>" }`
  - 不能用 `wiki_entry_list` 格式

### 3. note_id不一致
- **问题**：`import_doc` 返回的 `note_id` 与 `list_note` 返回的不同
- **解决**：必须以 `list_note` 返回的为准

### 4. OCR太慢
- **问题**：单进程处理171张图片需2小时+
- **解决**：使用multiprocessing，4进程可将时间缩短至25分钟

### 5. HEIC格式无法读取
- **问题**：PIL无法直接读取HEIC
- **解决**：安装 `pillow-heif`，先调用 `register_heif_opener()`

## 输出文件

- `ocr_results.txt`：完整OCR结果（按图片分节）
- 9篇详细笔记：每篇3000-5000字，通过import_doc API创建

## 参考资源

### scripts/
- 无（脚本建议在工作时动态生成，避免硬编码）

### references/
- `api_reference.md`：IMA OpenAPI接口详细说明

### assets/
- 无
