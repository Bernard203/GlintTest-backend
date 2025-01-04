import requests
import json

API_KEY = "your_api_key"
SECRET_KEY = "your_secret_key"
BASE_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-4.0-8k-latest"


def get_access_token():
    """
    获取百度文心一言的 Access Token。
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY
    }
    response = requests.post(url, params=params).json()
    return response.get("access_token")


def generate_test_operations(json_data, scene_description):
    """
    调用文心一言生成测试操作。

    :param json_data: 当前 UI 的组件信息（JSON 格式）
    :param scene_description: 场景描述
    :return: 生成的测试操作
    """
    access_token = get_access_token()
    if not access_token:
        print("Failed to retrieve access token.")
        return None

    prompt = f"""
    根据以下 UI 组件和目标场景生成测试操作：
    目标场景：{scene_description}
    UI 组件信息：{json.dumps(json_data, ensure_ascii=False)}
    请生成 ADB 命令来实现该场景。
    """

    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({
        "messages": [{"role": "user", "content": prompt}]
    }, ensure_ascii=False)
    url = f"{BASE_URL}?access_token={access_token}"
    response = requests.post(url, headers=headers, data=payload.encode('utf-8'))
    if response.status_code == 200:
        return response.json().get("result", "")
    else:
        print(f"Failed to generate operations: {response.status_code}")
        return None
