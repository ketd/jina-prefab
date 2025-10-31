# Jina AI 预制件使用示例

本预制件提供了两个核心功能，使用 Jina AI 的 API 进行网络搜索和 URL 内容读取。

## 前置要求

1. 获取 Jina API Key：访问 https://jina.ai/ 注册账号并创建 API Key
2. 在平台上配置环境变量 `JINA_API_KEY`

## 函数说明

### 1. jina_search - 网络搜索

使用 Jina Search API 进行网络搜索。

**参数：**
- `query` (string, 必需): 搜索关键词或问题
- `max_results` (integer, 可选): 返回的最大结果数量，默认 10
- `include_content` (boolean, 可选): 是否包含页面内容，默认 false

**返回示例：**

```json
{
  "success": true,
  "query": "Jina AI",
  "results": [
    {
      "title": "Jina AI - Your Search Foundation, Supercharged.",
      "url": "https://jina.ai/",
      "description": "Best-in-class embeddings, rerankers, web reader...",
      "content": ""
    }
  ],
  "total_results": 1,
  "total_tokens": 100
}
```

**使用场景：**
- 网络信息搜索
- 实时资讯获取
- 竞品分析
- 知识问答辅助

### 2. jina_read_url - 读取 URL 内容

使用 Jina Reader API 读取指定 URL 的内容。

**参数：**
- `url` (string, 必需): 要读取的 URL 地址（必须以 http:// 或 https:// 开头）
- `include_metadata` (boolean, 可选): 是否包含页面元数据，默认 true

**返回示例：**

```json
{
  "success": true,
  "url": "https://www.example.com/",
  "title": "Example Domain",
  "description": "Example description",
  "content": "This domain is for use in documentation...",
  "published_time": "Thu, 09 Oct 2025 16:42:02 GMT",
  "metadata": {
    "lang": "en",
    "viewport": "width=device-width, initial-scale=1"
  },
  "tokens": 29
}
```

**使用场景：**
- 网页内容提取
- 文章阅读和总结
- 竞品内容分析
- 知识库构建

## 错误处理

所有函数都包含完善的错误处理：

```json
{
  "success": false,
  "error": "错误描述",
  "error_code": "ERROR_CODE"
}
```

**常见错误代码：**
- `MISSING_API_KEY`: 未配置 API Key
- `INVALID_API_KEY`: API Key 无效或已过期
- `RATE_LIMIT_EXCEEDED`: API 调用频率超限
- `REQUEST_TIMEOUT`: 请求超时
- `CONNECTION_ERROR`: 网络连接失败

## 本地测试

```bash
# 1. 安装依赖
uv sync --dev

# 2. 设置环境变量
export JINA_API_KEY="your_api_key_here"

# 3. 运行测试
uv run pytest tests/ -v

# 4. 运行验证
uv run python scripts/validate_manifest.py
```

## Python 代码示例

```python
from src.main import jina_search, jina_read_url

# 搜索示例
result = jina_search(
    query="Python tutorial",
    max_results=5,
    include_content=False
)

if result["success"]:
    for item in result["results"]:
        print(f"标题: {item['title']}")
        print(f"URL: {item['url']}")
        print(f"描述: {item['description']}")
        print("---")

# 读取 URL 示例
result = jina_read_url(
    url="https://www.example.com",
    include_metadata=True
)

if result["success"]:
    print(f"标题: {result['title']}")
    print(f"内容: {result['content'][:200]}...")
    print(f"使用 Tokens: {result['tokens']}")
```

## 性能提示

1. **不包含内容**: 如果只需要标题和描述，设置 `include_content=False` 可以节省 tokens
2. **限制结果数**: 合理设置 `max_results` 可以减少响应时间和 token 消耗
3. **错误重试**: 遇到 `RATE_LIMIT_EXCEEDED` 时应该实现指数退避重试策略

## 注意事项

- Jina AI API 可能有使用配额限制
- 确保 URL 格式正确（必须包含 http:// 或 https://）
- 某些网站可能无法被 Jina Reader 访问（如需要登录的页面）
- API 响应时间取决于网络状况和目标网站的复杂度

