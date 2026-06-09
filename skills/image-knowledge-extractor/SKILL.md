---
name: image-knowledge-extractor
description: 从任意图片文件夹中批量提取文字（OCR）、按用户指定类别或标签整理、输出为Markdown报告或上传至指定笔记/知识库平台的全流程自动化技能。支持HEIC/JPG/PNG/WEBP/GIF/BMP等格式。平台包括：IMA知识库、Notion、Obsidian目录、纯Markdown文件输出。适用于：1）批量处理手机截图中的知识内容；2）OCR识别文档/照片文字；3）将提取内容分类整理为结构化笔记；4）上传至IMA/Notion/Obsidian等平台。触发词：整理图片知识、图片OCR、截图整理、知识提取、批量提取图片文字、截图转文字、从图片提取内容。
agent_created: true
---

# 图片知识提取与多平台上传

## 概述

本技能提供从图片文件夹批量提取文字并上传至任意平台的完整工作流。支持多进程OCR加速、HEIC格式读取、断点续跑、增量写入，以及多种输出格式（Markdown报告、IMA知识库、Notion、Obsidian）。

## 前置条件

### 运行时环境
- Python 3.10+（建议使用隔离venv）
- Node.js 18+（仅IMA平台需要）

### 依赖安装
```bash
pip install rapidocr-onnxruntime pillow-heif python-dotenv
```

- **rapidocr-onnxruntime**：中文OCR引擎，支持中英文混合
- **pillow-heif**：读取HEIC/HEIF格式（iPhone截图）
- **python-dotenv**：管理不同平台的API密钥（可选）

### 支持的平台与所需依赖

| 平台 | 需要 | 说明 |
|------|------|------|
| 纯Markdown文件 | 无 | 本地输出 |
| Obsidian目录 | 无 | 本地目录 |
| IMA知识库 | Node.js + ima_api.cjs | 使用OpenAPI |
| Notion | `pip install notion-client` | 使用Notion API |

## 工作流程

### 第1步：确认配置参数

在开始之前，向用户确认以下信息：

1. **图片文件夹路径**：`IMAGE_DIR`
2. **输出平台**：`--platform`（markdown/obsidian/ima/notion/none）
3. **输出路径**：`OUTPUT_PATH`
4. **分类方式**：`--category-mode`
   - `auto`：自动按AI/编程/科研等类别分类（默认）
   - `manual`：用户手动指定类别
   - `tags`：按标签分类，不分组
   - `none`：不分分类，直接输出

5. **OCR置信度阈值**：`CONFIDENCE_THRESHOLD`（默认0.3，范围0.0-1.0）
6. **并行进程数**：`NUM_WORKERS`（默认CPU核心数）

如果用户未指定平台，默认输出为Markdown文件。

### 第2步：生成OCR脚本

根据配置生成多进程OCR脚本。脚本核心逻辑：

```python
# 核心配置
IMAGE_DIR = "绝对路径"
OUTPUT_FILE = "输出文件路径"
NUM_WORKERS = 4
CONFIDENCE_THRESHOLD = 0.3

# 支持的文件格式
IMAGE_EXTENSIONS = {'.heic', '.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp', '.tiff', '.tif'}
```

**脚本特性**：
- 多进程：`multiprocessing.Pool` + `initializer`（per-worker模型加载）
- 增量写入：实时追加到输出文件
- 断点续跑：跳过已处理文件（通过checkpoint.json记录）
- HEIC支持：`pillow-heif.register_heif_opener()`

### 第3步：执行OCR识别

```bash
python ocr_script.py
```

**输出格式**：
```markdown
## filename.jpg

识别文字内容第1行
识别文字内容第2行
...

## IMG_1234.HEIC

识别文字内容第1行
...
```

### 第4步：读取并分类OCR结果

读取完整OCR结果，按用户指定的方式分类。

#### 自动分类模式（默认）

按以下类别自动分类（可根据内容调整）：

| 类别 | 关键词 |
|------|--------|
| AI与大模型工具 | 大模型、API、LLM、ChatGPT、Gemini、Claude、GPT-4 |
| AI编程工具 | Skills、Agent、TRAE、Cursor、Copilot、Hermes |
| 编程开发 | Python、JavaScript、代码、GitHub、开源 |
| 科研学术 | 论文、学术、research、citation、bib |
| 开源项目 | stars、github、repo、开源项目 |
| 办公效率 | PPT、PDF、Excel、Word、Notion、Obsidian |
| 职场/法律 | 劳动法、维权、辞职、合同、社保 |
| 生活技巧 | 教程、攻略、生活、工具推荐 |
| 3D/设计/视频 | Blender、C4D、视频、3D、设计 |
| 网络资源 | 激活、免费、入口、网站、资源 |
| 其他 | 无法归类的 |

#### 手动分类模式

用户提供类别列表，按类别筛选。

#### 标签模式

提取关键词作为标签，不创建分组。

### 第5步：输出内容

#### 平台：Markdown / Obsidian

生成结构化Markdown文件，按类别分节：

```markdown
# 图片提取知识报告

## AI与大模型工具生态
> 来源：IMG_001.jpg, IMG_005.HEIC

**工具名称** - 描述...
...

## 编程开发
> 来源：IMG_002.png, IMG_003.jpg

**工具名称** - 描述...
...
```

**Obsidian模式**：每篇笔记保存为独立文件（`notes/{category}/{title}.md`），含源文件链接。

#### 平台：IMA知识库

使用IMA OpenAPI（详见 `references/api_reference.md`）：

1. 按类别创建笔记（`import_doc` API）
2. 获取正确note_id（`list_note` API）
3. 添加到知识库（`add_knowledge` API）

**关键参数**：
- `content_format`: 1 = MARKDOWN
- `note_info.content_id`: 必须是`list_note`返回的ID
- `knowledge_base_id`: 必须base64格式

**知识库ID获取**：
```bash
ima_api.cjs "openapi/wiki/v1/search_knowledge" '{"page":{"page_num":1,"page_size":20},"keyword":"keyword"}'
```

**凭证管理**：
- 清除 `~/.config/ima/client_id` 和 `api_key` 的BOM
- 首次调用设置 `IMA_FORCE_UPDATE_CHECK=1`

#### 平台：Notion

使用Notion API（需要 `notion-client`）：

1. 获取 `NOTION_API_KEY` 和 `NOTION_DATABASE_ID`
2. 每篇笔记作为数据库条目创建
3. 或作为独立页面创建

```python
import notion_client

client = notion_client.Client(token=os.environ["NOTION_API_KEY"])

# 在数据库中创建页面
client.pages.create(
    parent={"database_id": "DATABASE_ID"},
    properties={
        "Title": {"title": [{"text": {"content": "标题"}}]},
        "Category": {"select": {"name": "AI与工具"}},
    },
    children={
        "pages": [{"object": "page", "parent": {"type": "page_id", "page_id": "PAGE_ID"}, "content": [...]}]
    }
)
```

### 第6步：验证结果

根据输出平台选择验证方式：

- **Markdown/Obsidian**：检查文件数量和大小
- **IMA**：调用 `get_doc_content` 和 `search_knowledge` 验证
- **Notion**：在Notion中查看页面是否创建

## 常见问题与解决方案

### 1. OCR结果质量差
- 检查图片分辨率（建议>720p）
- 降低置信度阈值（0.3→0.1）
- 确保图片文字清晰、无严重模糊

### 2. HEIC格式无法读取
- 安装 `pillow-heif`
- 先调用 `register_heif_opener()`
- 或先将HEIC转为JPG

### 3. IMA API认证失败
- 清除凭证文件BOM
- 设置 `IMA_FORCE_UPDATE_CHECK=1`

### 4. Notion API权限问题
- 检查API Key权限范围
- 确保数据库已共享给API Key

### 5. OCR太慢
- 增加 `NUM_WORKERS`
- 4进程可将171张图片处理时间从2小时+降至25分钟

### 6. 图片数量很多（>500张）
- 分批处理（每次100-200张）
- 使用checkpoint机制断点续跑
- 输出文件按批次分卷

## 输出格式配置

### 完整模式（默认）
- 每个类别单独文件/笔记
- 包含完整OCR文字
- 标注来源文件

### 精简模式
- 仅保留高置信度内容
- 每个类别摘要式输出
- 标注来源文件

### 标签模式
- 所有图片内容输出为单一文件
- 添加来源标签（`#IMG_001`）
- 支持按标签搜索

## 参考资源

### scripts/
- 无（脚本建议在工作时动态生成，避免硬编码）

### references/
- `api_reference.md`：IMA OpenAPI和Notion API接口参考

### assets/
- 无
