"""
测试预制件核心功能

测试说明：
- 这些测试演示了基本的测试结构
- 实际测试时需要配置 JINA_API_KEY 环境变量
- 可以使用 mock 来模拟 API 响应
"""

import os
from unittest.mock import MagicMock, patch

import pytest

from src.main import jina_read_url, jina_search


class TestJinaSearch:
    """测试 jina_search 函数"""

    def test_search_missing_api_key(self):
        """测试缺少 API Key 的情况"""
        # 确保环境变量中没有 API Key
        with patch.dict(os.environ, {}, clear=True):
            result = jina_search(query="test")

        assert result["success"] is False
        assert result["error_code"] == "MISSING_API_KEY"

    def test_search_invalid_query(self):
        """测试无效的查询参数"""
        with patch.dict(os.environ, {"JINA_API_KEY": "test_key"}):
            # 空字符串
            result = jina_search(query="")
            assert result["success"] is False
            assert result["error_code"] == "INVALID_QUERY"

            # 只有空格
            result = jina_search(query="   ")
            assert result["success"] is False
            assert result["error_code"] == "INVALID_QUERY"

    def test_search_invalid_max_results(self):
        """测试无效的 max_results 参数"""
        with patch.dict(os.environ, {"JINA_API_KEY": "test_key"}):
            # 零
            result = jina_search(query="test", max_results=0)
            assert result["success"] is False
            assert result["error_code"] == "INVALID_MAX_RESULTS"

            # 负数
            result = jina_search(query="test", max_results=-1)
            assert result["success"] is False
            assert result["error_code"] == "INVALID_MAX_RESULTS"

    @patch("src.main.requests.get")
    def test_search_success(self, mock_get):
        """测试成功的搜索请求"""
        # 模拟成功的 API 响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 200,
            "status": 20000,
            "data": [
                {
                    "title": "Test Title",
                    "url": "https://example.com",
                    "description": "Test description",
                    "content": ""
                }
            ],
            "meta": {
                "usage": {
                    "tokens": 100
                }
            }
        }
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {"JINA_API_KEY": "test_key"}):
            result = jina_search(query="test query")

        assert result["success"] is True
        assert result["query"] == "test query"
        assert len(result["results"]) == 1
        assert result["results"][0]["title"] == "Test Title"
        assert result["total_tokens"] == 100

    @patch("src.main.requests.get")
    def test_search_with_content(self, mock_get):
        """测试包含内容的搜索请求"""
        # 模拟成功的 API 响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 200,
            "status": 20000,
            "data": [
                {
                    "title": "Test Title",
                    "url": "https://example.com",
                    "description": "Test description",
                    "content": "Test content"
                }
            ],
            "meta": {
                "usage": {
                    "tokens": 200
                }
            }
        }
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {"JINA_API_KEY": "test_key"}):
            result = jina_search(query="test", include_content=True)

        assert result["success"] is True
        assert result["results"][0]["content"] == "Test content"

    @patch("src.main.requests.get")
    def test_search_rate_limit(self, mock_get):
        """测试 API 频率限制"""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {"JINA_API_KEY": "test_key"}):
            result = jina_search(query="test")

        assert result["success"] is False
        assert result["error_code"] == "RATE_LIMIT_EXCEEDED"

    @patch("src.main.requests.get")
    def test_search_invalid_api_key(self, mock_get):
        """测试无效的 API Key"""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {"JINA_API_KEY": "invalid_key"}):
            result = jina_search(query="test")

        assert result["success"] is False
        assert result["error_code"] == "INVALID_API_KEY"


class TestJinaReadUrl:
    """测试 jina_read_url 函数"""

    def test_read_url_missing_api_key(self):
        """测试缺少 API Key 的情况"""
        with patch.dict(os.environ, {}, clear=True):
            result = jina_read_url(url="https://example.com")

        assert result["success"] is False
        assert result["error_code"] == "MISSING_API_KEY"

    def test_read_url_invalid_url(self):
        """测试无效的 URL"""
        with patch.dict(os.environ, {"JINA_API_KEY": "test_key"}):
            # 空字符串
            result = jina_read_url(url="")
            assert result["success"] is False
            assert result["error_code"] == "INVALID_URL"

            # 只有空格
            result = jina_read_url(url="   ")
            assert result["success"] is False
            assert result["error_code"] == "INVALID_URL"

            # 缺少协议
            result = jina_read_url(url="example.com")
            assert result["success"] is False
            assert result["error_code"] == "INVALID_URL_FORMAT"

    @patch("src.main.requests.get")
    def test_read_url_success(self, mock_get):
        """测试成功读取 URL"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 200,
            "status": 20000,
            "data": {
                "title": "Example Domain",
                "description": "Example description",
                "url": "https://www.example.com/",
                "content": "Example content",
                "publishedTime": "Thu, 09 Oct 2025 16:42:02 GMT",
                "metadata": {
                    "lang": "en",
                    "viewport": "width=device-width, initial-scale=1"
                },
                "usage": {
                    "tokens": 29
                }
            },
            "meta": {
                "usage": {
                    "tokens": 29
                }
            }
        }
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {"JINA_API_KEY": "test_key"}):
            result = jina_read_url(url="https://www.example.com")

        assert result["success"] is True
        assert result["title"] == "Example Domain"
        assert result["content"] == "Example content"
        assert result["tokens"] == 29
        assert "metadata" in result
        assert result["metadata"]["lang"] == "en"

    @patch("src.main.requests.get")
    def test_read_url_without_metadata(self, mock_get):
        """测试不包含元数据的请求"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 200,
            "status": 20000,
            "data": {
                "title": "Example Domain",
                "description": "",
                "url": "https://www.example.com/",
                "content": "Example content",
                "publishedTime": "",
                "metadata": {
                    "lang": "en"
                },
                "usage": {
                    "tokens": 29
                }
            }
        }
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {"JINA_API_KEY": "test_key"}):
            result = jina_read_url(url="https://www.example.com", include_metadata=False)

        assert result["success"] is True
        assert "metadata" not in result

    @patch("src.main.requests.get")
    def test_read_url_not_found(self, mock_get):
        """测试 URL 不存在"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {"JINA_API_KEY": "test_key"}):
            result = jina_read_url(url="https://example.com/notfound")

        assert result["success"] is False
        assert result["error_code"] == "URL_NOT_FOUND"

    @patch("src.main.requests.get")
    def test_read_url_rate_limit(self, mock_get):
        """测试 API 频率限制"""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {"JINA_API_KEY": "test_key"}):
            result = jina_read_url(url="https://example.com")

        assert result["success"] is False
        assert result["error_code"] == "RATE_LIMIT_EXCEEDED"

    @patch("src.main.requests.get")
    def test_read_url_invalid_api_key(self, mock_get):
        """测试无效的 API Key"""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {"JINA_API_KEY": "invalid_key"}):
            result = jina_read_url(url="https://example.com")

        assert result["success"] is False
        assert result["error_code"] == "INVALID_API_KEY"
