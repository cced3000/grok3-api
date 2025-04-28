from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import uvicorn
from typing import Dict, Any, Optional

from grok_client import GrokClient

app = FastAPI(title="Grok API", description="API for interacting with Grok-3 model")

cookie_str = "i18nextLng=zh; _ga=GA1.1.248121545.1745831149; cf_clearance=k9Wp1qTsaTVUKZz1N_nGTKVClm6gdRFCIxU6PxBxSzk-1745831203-1.2.1.1-Np.78HM1d40dq6P3FWDMywAit5YVA2OleATPZ9T6C9H8g8fO9eC0YbiDatryZWq68Narve4ooIrdhpFwYkZIXBWFHqHyt7jOrb8bEb0ctuRRFKMqE9wR40RJkLs_5mLjRlFbjp6aM86YuU7_J_LeS6WAzCvTZjlAPJJdG9OKPiLKGAH0d3sU0656mu8Dzk7nc9jKMls8f6D9IwfzH_q9dpz4G6COXlobKMSITlIN4XDnHM2JrjrwKOQiIDUfAMWIGCBiuXr5zuElXQa449.uE2rW1hxahTX7zuia2Usm322vqZRYRiHzwlUnAKzf2vVwE05vAB8p8jGVqmI7f98gjbGUqVdDagjMKIA.zW5Q5AFhiFFVi2hFoD9Fo06s4xv7; sso-rw=eyJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uX2lkIjoiZGJiMjZkMjAtMjczNS00NjBiLWE3ODQtMDJlZDliNDM2MTQ3In0.azZJ2V2QofmTeBA3VRrGUcf63HRp8hHSy3IJODQzhdM; sso=eyJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uX2lkIjoiZGJiMjZkMjAtMjczNS00NjBiLWE3ODQtMDJlZDliNDM2MTQ3In0.azZJ2V2QofmTeBA3VRrGUcf63HRp8hHSy3IJODQzhdM; _ga_8FEWB057YH=GS1.1.1745831149.1.1.1745831661.0.0.0"
grok_client = GrokClient.from_cookie_string(cookie_str)
 

class GrokRequest(BaseModel):
    """请求模型，用于接收用户消息"""
    content: str
    cookies: Optional[Dict[str, str]] = None


class GrokResponse(BaseModel):
    """响应模型，用于返回Grok的回复"""
    response: str


@app.post("/api/grok", response_model=GrokResponse)
async def send_to_grok_post(request: GrokRequest):
    """通过POST请求体发送消息到Grok并获取响应

    Args:
        request: 包含用户消息和可选cookie的请求对象

    Returns:
        包含Grok响应的对象
    """
    try:
        # 使用请求体中的内容
        message_content = request.content
        
        # 如果提供了自定义cookie，则使用它们创建新的客户端实例
        client = grok_client
        if request.cookies:
            client = GrokClient(request.cookies)
            
        # 发送消息并获取响应
        response = client.send_message(message_content)
        return GrokResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"与Grok通信时出错: {str(e)}")

 

@app.get("/")
async def root():
    """API根路径，返回简单的欢迎信息"""
    return {"message": "欢迎使用Grok API，请使用 /api/grok 端点发送消息"}


if __name__ == "__main__":
    # 启动FastAPI应用
    uvicorn.run(app, host="0.0.0.0", port=8000)