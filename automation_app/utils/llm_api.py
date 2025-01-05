import requests
import json

# Step 1: 配置文心一言 API 密钥和 URL
API_KEY = "lzra11x5pmhrIjkXLJLRTQEJ"  # 替换为你的 API Key
SECRET_KEY = "I8JoKF7mfFFSWTR0OUMx21t8bwi9MoGJ"  # 替换为你的 Secret Key
BASE_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-4.0-8k-latest"  # 修改为正确的 URL


# Step 2: 获取 Access Token
def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY
    }
    response = requests.post(url, params=params).json()
    access_token = response.get("access_token")
    if not access_token:
        print("Error: Failed to get access token:", response)
    return access_token


# Step 3: 读取 JSON 文件
def read_json_file(file_path="../output/components.json"):
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    return json_data


# Step 4: 使用文心一言生成测试操作
def generate_test_operations(json_data, scene_description):
    access_token = get_access_token()

    prompt = f"""
    You are an intelligent GUI testing assistant. Based on the provided JSON file and scene description, please analyze the current application's UI components and generate the necessary ADB commands to automate the testing process.

    Goal Scene: {scene_description}

    UI components data:
    {json.dumps(json_data, ensure_ascii=False)}

    The sequence of operations should be as follows:
    - Before inputting any text, make sure to click on the input field (e.g., "Enter your phone number") to activate it.
    - Input actions (e.g., entering text into the input field)
    - Button clicks
    - Swipe actions (if any)

    Please generate the test operations for this scenario, including but not limited to:
    1. Operation type (e.g., "input", "click")
    2. Description of the target component (e.g., input field placeholder, button label)
    3. The specific execution action (e.g., text to input, coordinates to click)

    The output should be formatted as follows:

    1. **Operation Type**: [operation_type]
       - **Target Component**: [component_description]
       - **Execution**: [specific_action]
       - **ADB Command**: [generated_adb_command]

    If you want to generate a phone number in China, you need to generate it in the format of "13301995011" without the country code "+86".



    After entering the phone number in the login operation, you need to click the button below the input field.
    After entering the text into the input field, I need to click on a blank area.

    Please respond with only the ADB command for each operation.
    Do not include any additional content, including descriptions or tips, after the ADB command.
    """

    payload = json.dumps({
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "penalty_score": 1,
        "enable_system_memory": False,
        "disable_search": False,
        "enable_citation": False,
        "enable_trace": False
    }, ensure_ascii=False)

    headers = {
        'Content-Type': 'application/json'
    }

    url = f"{BASE_URL}?access_token={access_token}"

    response = requests.post(url, headers=headers, data=payload.encode("utf-8"))

    if response.status_code == 200:
        operations = response.json().get("result", "")
        return operations

    else:
        print("Request failed, status code:", response.status_code)