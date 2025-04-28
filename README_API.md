# Grok-3 API

这是一个基于FastAPI构建的简单API，用于与Grok-3大语言模型进行交互。该API封装了Grok客户端，提供了一个HTTP接口来发送消息并获取Grok的响应。

## 功能特点

- 简单的HTTP API接口
- 支持自定义cookie配置
- 完整的错误处理
- 基于Pydantic的请求和响应验证

## 安装

1. 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

在`api.py`文件中，您可以更新默认的cookie值：

```python
DEFAULT_COOKIES = {
    "x-anonuserid": "your-value",
    "x-challenge": "your-value",
    "x-signature": "your-value",
    "sso": "your-value",
    "sso-rw": "your-value"
}
```

## 运行API

```bash
python api.py
```

或者使用uvicorn直接运行：

```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

服务器将在 http://localhost:8000 上启动。

## API使用

### 发送消息到Grok

**端点**: `POST /api/grok`

**请求体**:

```json
{
  "content": "你的消息内容",
  "cookies": {  // 可选，如果不提供则使用默认配置
    "x-anonuserid": "your-value",
    "x-challenge": "your-value",
    "x-signature": "your-value",
    "sso": "your-value",
    "sso-rw": "your-value"
  }
}
```

**响应**:

```json
{
  "response": "Grok的回复内容"
}
```

### 示例

使用curl发送请求：

```bash
curl -X POST "http://localhost:8000/api/grok" \
     -H "Content-Type: application/json" \
     -d '{"content":"你好，Grok！"}'
```

使用Python requests库：

```python
import requests
import json

url = "http://localhost:8000/api/grok"
data = {"content": "你好，Grok！"}

response = requests.post(url, json=data)
print(json.loads(response.text)["response"])
```

## API文档

启动服务器后，您可以访问自动生成的API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 注意事项

- 请确保您有有效的Grok cookie值
- API默认在所有网络接口上监听，如果只需要本地访问，请将host更改为"127.0.0.1"
- 在生产环境中使用时，请考虑添加适当的安全措施，如API密钥验证