# IMA OpenAPI 接口参考

## 笔记相关接口

### 1. import_doc - 创建笔记

**接口**：`openapi/note/v1/import_doc`

**方法**：POST

**参数**：
```json
{
  "title": "笔记标题",
  "content": "# Markdown格式内容",
  "content_format": 1
}
```

**content_format 值**：
- `1` = MARKDOWN
- 不是字符串 "markdown"，必须是数字 1

**返回**：
```json
{
  "note_id": "7469999350357359",
  "success": true
}
```

**注意**：
- API返回的 `note_id` 与实际保存的笔记ID不一致
- 必须以 `list_note` 返回的 `note_id` 为准

---

### 2. list_note - 列出所有笔记

**接口**：`openapi/note/v1/list_note`

**方法**：POST

**参数**：
```json
{
  "folder_id": "",
  "cursor": "",
  "limit": 100
}
```

**返回**：
```json
{
  "items": [
    {
      "note_id": "7469993801316944",
      "title": "笔记标题",
      ...
    }
  ],
  "total": 9
}
```

**用途**：
- 获取正确的 `note_id`（用于 add_knowledge）
- 检查笔记是否已创建

---

### 3. get_doc_content - 获取笔记内容

**接口**：`openapi/note/v1/get_doc_content`

**方法**：POST

**参数**：
```json
{
  "note_id": "7469999350357359",
  "target_content_format": 0
}
```

**target_content_format 值**：
- `0` = 原始格式
- `1` = Markdown格式

---

### 4. delete_note - 删除笔记

**注意**：IMA 不支持笔记删除功能，API 返回 404。

---

## 知识库相关接口

### 1. add_knowledge - 添加笔记到知识库

**接口**：`openapi/wiki/v1/add_knowledge`

**方法**：POST

**参数**：
```json
{
  "media_type": 11,
  "note_info": {
    "content_id": "7469993801316944"
  },
  "title": "笔记标题",
  "knowledge_base_id": "InvlbvCKbDPjQTRorNwt87cC8p7EPmpGbHulGb3pWlc="
}
```

**关键参数**：
- `media_type`: `11` = 笔记
- `note_info.content_id`: 必须使用 `list_note` 返回的 `note_id`
- `knowledge_base_id`: 必须使用 **base64格式**，不是数字ID
- `title`: 可选，但建议提供

**知识库ID格式**：
- MCP工具返回：`7469983902738366`（数字ID）
- Wiki API需要：`InvlbvCKbDPjQTRorNwt87cC8p7EPmpGbHulGb3pWlc=`（base64格式）

**错误处理**：
- `invalid knowledge_base_id`: 使用了错误的格式或ID
- `invalid KnowledgeBaseId: value length must be at least 1 runes`: 使用了 `wiki_entry_list` 格式而非 `note_info`

---

### 2. search_knowledge - 搜索知识库

**接口**：`openapi/wiki/v1/search_knowledge`

**方法**：POST

**参数**（搜索知识库）：
```json
{
  "page": {"page_num": 1, "page_size": 20},
  "keyword": "日常"
}
```

**参数**（搜索知识库内容）：
```json
{
  "page": {"page_num": 1, "page_size": 20},
  "keyword": "",
  "knowledge_base_id": "InvlbvCKbDPjQTRorNwt87cC8p7EPmpGbHulGb3pWlc="
}
```

**用途**：
- 获取知识库的base64格式ID
- 查看知识库中的笔记列表

---

### 3. delete_note_from_wiki - 从知识库删除笔记

**注意**：IMA 不支持笔记删除功能。

---

## 环境变量

### IMA_FORCE_UPDATE_CHECK

首次调用IMA API时必须设置：
```bash
IMA_FORCE_UPDATE_CHECK=1 node ima_api.cjs "endpoint" 'params'
```

此环境变量用于强制检查API版本，首次调用时必需。

---

## 凭证管理

### 凭证文件位置

- `~/.config/ima/client_id`
- `~/.config/ima/api_key`

### 清除BOM

凭证文件可能包含UTF-8 BOM，导致认证失败。使用以下命令清除：

```python
import pathlib

for f in ["client_id", "api_key"]:
    path = pathlib.Path.home() / ".config" / "ima" / f
    content = path.read_bytes()
    if content.startswith(b'\xef\xbb\xbf'):
        path.write_bytes(content[3:])
        print(f"清除 {f} 的BOM")
    else:
        print(f"{f} 无需清除BOM")
```

---

## 使用示例

### 完整调用流程

```bash
# 1. 设置环境变量
export IMA_FORCE_UPDATE_CHECK=1

# 2. 创建笔记
node ima_api.cjs "openapi/note/v1/import_doc" '{
  "title": "AI与大模型工具生态",
  "content": "# 详细内容（Markdown格式）...",
  "content_format": 1
}'

# 3. 获取正确的note_id
node ima_api.cjs "openapi/note/v1/list_note" '{
  "folder_id": "",
  "cursor": "",
  "limit": 100
}'

# 4. 添加到知识库
node ima_api.cjs "openapi/wiki/v1/add_knowledge" '{
  "media_type": 11,
  "note_info": {"content_id": "<从list_note获取的note_id>"},
  "title": "AI与大模型工具生态",
  "knowledge_base_id": "InvlbvCKbDPjQTRorNwt87cC8p7EPmpGbHulGb3pWlc="
}'

# 5. 验证
node ima_api.cjs "openapi/note/v1/get_doc_content" '{
  "note_id": "<从list_note获取的note_id>",
  "target_content_format": 0
}'
```
