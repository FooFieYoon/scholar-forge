# 多平台API接口参考

## IMA OpenAPI

### 凭证管理

**凭证文件**：
- `~/.config/ima/client_id`
- `~/.config/ima/api_key`

**清除BOM**：
```python
import pathlib
for f in ["client_id", "api_key"]:
    path = pathlib.Path.home() / ".config" / "ima" / f
    content = path.read_bytes()
    if content.startswith(b'\xef\xbb\xbf'):
        path.write_bytes(content[3:])
```

**环境变量**：首次调用必须设置 `IMA_FORCE_UPDATE_CHECK=1`

### 笔记创建（import_doc）

```bash
IMA_FORCE_UPDATE_CHECK=1 node ima_api.cjs "openapi/note/v1/import_doc" '{
  "title": "笔记标题",
  "content": "# Markdown内容",
  "content_format": 1
}'
```

- `content_format`: 1 = MARKDOWN（数字，不是字符串）

### 获取正确note_id（list_note）

```bash
IMA_FORCE_UPDATE_CHECK=1 node ima_api.cjs "openapi/note/v1/list_note" '{
  "folder_id": "",
  "cursor": "",
  "limit": 100
}'
```

**重要**：API返回的note_id与实际保存的不同，必须以list_note返回的为准。

### 添加到知识库（add_knowledge）

```bash
IMA_FORCE_UPDATE_CHECK=1 node ima_api.cjs "openapi/wiki/v1/add_knowledge" '{
  "media_type": 11,
  "note_info": {"content_id": "<list_note返回的note_id>"},
  "title": "笔记标题",
  "knowledge_base_id": "<base64格式KB ID>"
}'
```

**关键点**：
- `note_info.content_id`：必须是list_note返回的ID
- `knowledge_base_id`：必须base64格式

**知识库ID获取**：
```bash
IMA_FORCE_UPDATE_CHECK=1 node ima_api.cjs "openapi/wiki/v1/search_knowledge" '{
  "page": {"page_num": 1, "page_size": 20},
  "keyword": "知识库名称"
}'
```

### 验证内容（get_doc_content）

```bash
IMA_FORCE_UPDATE_CHECK=1 node ima_api.cjs "openapi/note/v1/get_doc_content" '{
  "note_id": "<note_id>",
  "target_content_format": 0
}'
```

---

## Notion API

### 认证

需要两个环境变量：
- `NOTION_API_KEY`：Integration Token（Bearer）
- `NOTION_DATABASE_ID`：目标数据库ID（可选，可创建独立页面）

### 创建页面（独立页面）

```python
import notion_client
client = notion_client.Client(token=os.environ["NOTION_API_KEY"])

page = client.pages.create(
    parent={"workspace": "type": "workspace"},
    properties={"title": {"title": [{"text": {"content": "标题"}}]}},
    children={"content": [{"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"type": "text", "text": {"content": "标题"}}]}}]}
}
)
```

### 创建数据库条目

```python
client.pages.create(
    parent={"database_id": "DATABASE_ID"},
    properties={
        "Name": {"title": [{"text": {"content": "条目名称"}}]},
        "Category": {"select": {"name": "AI工具"}},
        "Source": {"multi_select": [{"name": "IMG_001"}]},
    },
    children={...}  # 页面内容
)
```

### 获取数据库列表

```bash
curl -H "Authorization: Bearer $NOTION_API_KEY" \
     -H "Content-Type: application/json" \
     https://api.notion.com/v1/databases
```

---

## Obsidian

Obsidian使用本地Markdown文件，无需API。

### 目录结构

```
obsidian_vault/
├── notes/
│   ├── AI与大模型/
│   │   └── GPT-4免费API.md
│   ├── 编程开发/
│   │   └── Python脚本优化.md
│   └── 科研学术/
│       └── 论文查重规则.md
└── tags.md
```

### 笔记格式

```markdown
---
tags: [AI工具, 大模型]
source: IMG_001.jpg, IMG_005.HEIC
created: 2026-06-09
---

# GPT-4免费API

## 内容

...
```
