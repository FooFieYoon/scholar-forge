# GitHub REST API 使用要点

通过 `gh api` 直接调用 GitHub REST API，避免 git clone/push 在 Windows 沙箱中的问题。

## 认证

```bash
gh auth status          # 检查登录状态
gh auth login --web     # 浏览器授权登录
gh auth token          # 获取 token（脚本中使用）
```

## 上传文件（PUT /contents）

**API 端点：** `PUT /repos/{owner}/{repo}/contents/{path}`

**创建新文件：**
```bash
# 1. 文件内容 Base64 编码
CONTENT=$(base64 -w0 local-file.txt)

# 2. 调用 API
gh api --method PUT "/repos/OWNER/REPO/contents/remote/path.txt" \
  --input - <<EOF
{
  "message": "Add remote/path.txt",
  "content": "$CONTENT"
}
EOF
```

**更新已存在文件（需要 SHA）：**
```bash
# 1. 先 GET 获取 SHA
SHA=$(gh api "/repos/OWNER/REPO/contents/remote/path.txt" --jq '.sha')

# 2. PUT 时带上 SHA
gh api --method PUT "/repos/OWNER/REPO/contents/remote/path.txt" \
  --input - <<EOF
{
  "message": "Update remote/path.txt",
  "content": "$CONTENT",
  "sha": "$SHA"
}
EOF
```

## 删除文件（DELETE /contents）

```bash
SHA=$(gh api "/repos/OWNER/REPO/contents/path/to/delete.txt" --jq '.sha')
gh api --method DELETE "/repos/OWNER/REPO/contents/path/to/delete.txt" \
  --input - <<EOF
{
  "message": "Delete path/to/delete.txt",
  "sha": "$SHA"
}
EOF
```

## 列出目录内容（GET /contents）

```bash
# 列出根目录
gh api "/repos/OWNER/REPO/contents" --jq '.[].name'

# 列出子目录
gh api "/repos/OWNER/REPO/contents/skills" --jq '.[].name'
```

## 注意事项

1. **Base64 编码不要用 `-w0`**（Windows 不支持），用 Python：
   ```python
   import base64
   with open("file.txt", "rb") as f:
       content_b64 = base64.b64encode(f.read()).decode("utf-8")
   ```

2. **不要在 `/tmp` 写临时文件**，Windows 沙箱会拦截 → 改用项目目录或用户目录

3. **大文件（>1MB）不能用 `/contents` API**，需要用 Git LFS 或直接 git push

4. **SHA 是必须的**（更新/删除时），先 GET 获取再传

5. **路径中的中文/特殊字符要 URL 编码**

## Python 脚本模板

```python
import base64, json, subprocess, urllib.request, urllib.error

def get_gh_token():
    result = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True)
    return result.stdout.strip()

def api_request(url, method="GET", data=None, token=None):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(url, headers=headers, method=method)
    if data is not None:
        req.data = json.dumps(data).encode("utf-8")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read()), None
    except urllib.error.HTTPError as e:
        return None, json.loads(e.read())
```
