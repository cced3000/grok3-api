import requests
import json

class GrokClient:
    @classmethod
    def from_cookie_string(cls, cookie_string):
        """
        从cookie字符串创建GrokClient实例
        
        Args:
            cookie_string (str): 浏览器cookie字符串，通常从curl命令或浏览器开发工具中获取
            
        Returns:
            GrokClient: 初始化好的客户端实例
        """
        return cls(cookie_string)
    def __init__(self, cookies=None):
        """
        Initialize the Grok client with cookie values

        Args:
            cookies (dict, optional): Dictionary containing cookie values or cookie string
                If a string is provided, it will be parsed as a cookie string
                If a dict is provided, it will be used directly
                If None is provided, no cookies will be sent
        """
        self.base_url = "https://grok.com/rest/app-chat/conversations/new"
        
        # 处理cookies参数
        if cookies is None:
            self.cookies = {}
        elif isinstance(cookies, str):
            # 解析cookie字符串
            self.cookies = {}
            for cookie in cookies.split('; '):
                if '=' in cookie:
                    name, value = cookie.split('=', 1)
                    self.cookies[name] = value
        else:
            # 假设cookies是一个字典
            self.cookies = cookies
        self.headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9",
            "baggage": "sentry-environment=production,sentry-release=q0ZH_dx0ViGh_uTOqhqM3,sentry-public_key=b311e0f2690c81f25e2c4cf6d4f7ce1c,sentry-trace_id=b1c6024a5e62419c934fb64fdbb6f0bd,sentry-sample_rate=0,sentry-sampled=false",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "dnt": "1",
            "origin": "https://grok.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://grok.com/",
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-arch": '"x86"',
            "sec-ch-ua-bitness": '"64"',
            "sec-ch-ua-full-version": '"135.0.7049.115"',
            "sec-ch-ua-full-version-list": '"Google Chrome";v="135.0.7049.115", "Not-A.Brand";v="8.0.0.0", "Chromium";v="135.0.7049.115"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": '""',
            "sec-ch-ua-platform": '"Windows"',
            "sec-ch-ua-platform-version": '"19.0.0"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sentry-trace": "b1c6024a5e62419c934fb64fdbb6f0bd-af8d38ef682a478f-0",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "x-xai-request-id": "9c0661f5-679e-4978-8b0f-a1cd319a7a2b"
        }

    def _prepare_payload(self, message):
        """Prepare the default payload with the user's message"""
        return {
            "temporary": True,
            "modelName": "grok-3",
            "message": message,
            "fileAttachments": [],
            "imageAttachments": [],
            "disableSearch": False,
            "enableImageGeneration": True,
            "returnImageBytes": False,
            "returnRawGrokInXaiRequest": False,
            "enableImageStreaming": True,
            "imageGenerationCount": 2,
            "forceConcise": False,
            "toolOverrides": {},
            "enableSideBySide": True,
            "sendFinalMetadata": True,
            "isReasoning": False,
            "webpageUrls": [],
            "disableTextFollowUps": True
        }

    def send_message(self, message):
        """
        Send a message to Grok and collect the streaming response

        Args:
            message (str): The user's input message

        Returns:
            str: The complete response from Grok
        """
        payload = self._prepare_payload(message)
        response = requests.post(
            self.base_url,
            headers=self.headers,
            cookies=self.cookies,
            json=payload,
            stream=True
        )

        # 检查响应状态
        if response.status_code != 200:
            return f"错误: API返回状态码 {response.status_code}"

        full_response = ""

        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                try:
                    json_data = json.loads(decoded_line)
                    result = json_data.get("result", {})
                    response_data = result.get("response", {})

                    # 检查是否有完整的模型响应
                    if "modelResponse" in response_data:
                        model_response = response_data["modelResponse"]
                        if isinstance(model_response, dict) and "message" in model_response:
                            return model_response["message"]
                        elif isinstance(model_response, str):
                            return model_response
                        else:
                            return str(model_response)

                    # 处理流式响应
                    token = response_data.get("token", "")
                    if token:
                        full_response += token

                except json.JSONDecodeError:
                    # 忽略无法解析的行
                    continue

        return full_response.strip()