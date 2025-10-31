"""
Jina AI 预制件

使用 Jina AI 的 API 实现网络搜索和 URL 内容读取功能。

功能：
- jina_search: 使用 Jina Search API 进行网络搜索
- jina_read_url: 使用 Jina Reader API 读取 URL 内容

完整开发指南请查看：AGENTS.md
"""

import os
from typing import Any, Dict

import requests


def jina_search(
    query: str,
    max_results: int = 10,
    include_content: bool = False
) -> dict:
    """
    使用 Jina AI 进行网络搜索

    这个函数使用 Jina Search API 搜索网络内容，返回相关的搜索结果。

    Args:
        query: 搜索关键词或问题
        max_results: 返回的最大结果数量，默认 10
        include_content: 是否包含页面内容（会消耗更多 tokens），默认 False

    Returns:
        包含搜索结果的字典，格式如下：
        {
            "success": True,
            "query": "搜索关键词",
            "results": [
                {
                    "title": "页面标题",
                    "url": "页面URL",
                    "description": "页面描述",
                    "content": "页面内容（可选）"
                }
            ],
            "total_tokens": 使用的总 tokens 数
        }

    Examples:
        >>> result = jina_search(query="Python tutorial")
        >>> print(result['results'][0]['title'])
        'Python Tutorial - W3Schools'

        >>> result = jina_search(query="AI news", max_results=5, include_content=True)
        >>> print(len(result['results']))
        5
    """
    try:
        # 从环境变量中获取 API Key
        api_key = os.environ.get('JINA_API_KEY')

        # 验证 API Key
        if not api_key:
            return {
                "success": False,
                "error": "未配置 JINA_API_KEY，请在平台上配置该密钥",
                "error_code": "MISSING_API_KEY"
            }

        # 验证参数
        if not query or not isinstance(query, str) or not query.strip():
            return {
                "success": False,
                "error": "query 参数必须是非空字符串",
                "error_code": "INVALID_QUERY"
            }

        if not isinstance(max_results, int) or max_results <= 0:
            return {
                "success": False,
                "error": "max_results 必须是大于 0 的整数",
                "error_code": "INVALID_MAX_RESULTS"
            }

        # 构建请求 URL
        base_url = "https://s.jina.ai/"
        params = {"q": query.strip()}

        # 构建请求头
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # 根据 include_content 参数设置响应格式
        if not include_content:
            headers["X-Respond-With"] = "no-content"

        # 发送请求
        response = requests.get(base_url, params=params, headers=headers, timeout=30)

        # 检查响应状态
        if response.status_code == 401:
            return {
                "success": False,
                "error": "JINA_API_KEY 无效或已过期",
                "error_code": "INVALID_API_KEY"
            }
        elif response.status_code == 429:
            return {
                "success": False,
                "error": "API 调用频率超限，请稍后重试",
                "error_code": "RATE_LIMIT_EXCEEDED"
            }
        elif response.status_code != 200:
            return {
                "success": False,
                "error": f"API 请求失败，状态码: {response.status_code}",
                "error_code": "API_REQUEST_FAILED",
                "status_code": response.status_code
            }

        # 解析响应
        data = response.json()

        # 检查响应格式
        if data.get("code") != 200:
            return {
                "success": False,
                "error": f"API 返回错误: {data.get('status', 'Unknown error')}",
                "error_code": "API_ERROR"
            }

        # 提取结果
        results = data.get("data", [])

        # 限制结果数量
        results = results[:max_results]

        # 计算总 tokens
        total_tokens = data.get("meta", {}).get("usage", {}).get("tokens", 0)

        return {
            "success": True,
            "query": query.strip(),
            "results": results,
            "total_results": len(results),
            "total_tokens": total_tokens
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "请求超时，请检查网络连接或稍后重试",
            "error_code": "REQUEST_TIMEOUT"
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "网络连接失败，请检查网络连接",
            "error_code": "CONNECTION_ERROR"
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"请求失败: {str(e)}",
            "error_code": "REQUEST_FAILED"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_code": "UNEXPECTED_ERROR"
        }


def jina_read_url(
    url: str,
    include_metadata: bool = True
) -> dict:
    """
    使用 Jina AI 读取 URL 内容

    这个函数使用 Jina Reader API 读取指定 URL 的内容，
    返回页面的标题、描述、正文内容等信息。

    Args:
        url: 要读取的 URL 地址
        include_metadata: 是否包含页面元数据（语言、viewport 等），默认 True

    Returns:
        包含页面内容的字典，格式如下：
        {
            "success": True,
            "url": "原始URL",
            "title": "页面标题",
            "description": "页面描述",
            "content": "页面正文内容（Markdown 格式）",
            "published_time": "发布时间",
            "metadata": {
                "lang": "语言",
                "viewport": "视口设置"
            },
            "tokens": 使用的 tokens 数
        }

    Examples:
        >>> result = jina_read_url(url="https://www.example.com")
        >>> print(result['title'])
        'Example Domain'

        >>> result = jina_read_url(url="https://blog.example.com/article", include_metadata=False)
        >>> print(result['content'])
        '# Article Title\\n\\nArticle content...'
    """
    try:
        # 从环境变量中获取 API Key
        api_key = os.environ.get('JINA_API_KEY')

        # 验证 API Key
        if not api_key:
            return {
                "success": False,
                "error": "未配置 JINA_API_KEY，请在平台上配置该密钥",
                "error_code": "MISSING_API_KEY"
            }

        # 验证参数
        if not url or not isinstance(url, str) or not url.strip():
            return {
                "success": False,
                "error": "url 参数必须是非空字符串",
                "error_code": "INVALID_URL"
            }

        # 验证 URL 格式
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            return {
                "success": False,
                "error": "url 必须以 http:// 或 https:// 开头",
                "error_code": "INVALID_URL_FORMAT"
            }

        # 构建请求 URL
        reader_url = f"https://r.jina.ai/{url}"

        # 构建请求头
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # 发送请求
        response = requests.get(reader_url, headers=headers, timeout=30)

        # 检查响应状态
        if response.status_code == 401:
            return {
                "success": False,
                "error": "JINA_API_KEY 无效或已过期",
                "error_code": "INVALID_API_KEY"
            }
        elif response.status_code == 429:
            return {
                "success": False,
                "error": "API 调用频率超限，请稍后重试",
                "error_code": "RATE_LIMIT_EXCEEDED"
            }
        elif response.status_code == 404:
            return {
                "success": False,
                "error": "目标 URL 不存在或无法访问",
                "error_code": "URL_NOT_FOUND"
            }
        elif response.status_code != 200:
            return {
                "success": False,
                "error": f"API 请求失败，状态码: {response.status_code}",
                "error_code": "API_REQUEST_FAILED",
                "status_code": response.status_code
            }

        # 解析响应
        data = response.json()

        # 检查响应格式
        if data.get("code") != 200:
            return {
                "success": False,
                "error": f"API 返回错误: {data.get('status', 'Unknown error')}",
                "error_code": "API_ERROR"
            }

        # 提取内容
        content_data = data.get("data", {})

        # 构建返回结果
        result: Dict[str, Any] = {
            "success": True,
            "url": content_data.get("url", url),
            "title": content_data.get("title", ""),
            "description": content_data.get("description", ""),
            "content": content_data.get("content", ""),
            "published_time": content_data.get("publishedTime", ""),
            "tokens": content_data.get("usage", {}).get("tokens", 0)
        }

        # 可选：添加元数据
        if include_metadata:
            result["metadata"] = content_data.get("metadata", {})

        # 可选：添加警告信息
        if "warning" in content_data:
            result["warning"] = content_data["warning"]

        return result

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "请求超时，请检查网络连接或稍后重试",
            "error_code": "REQUEST_TIMEOUT"
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "网络连接失败，请检查网络连接",
            "error_code": "CONNECTION_ERROR"
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"请求失败: {str(e)}",
            "error_code": "REQUEST_FAILED"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_code": "UNEXPECTED_ERROR"
        }
