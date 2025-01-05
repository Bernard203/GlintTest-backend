import time
from time import sleep

from .llm_api import generate_test_operations, read_json_file
from .state_validator import validate_operations
from .gui_executor import execute_adb_commands
from .screenshot_tools import capture_screenshot, extract_components
import threading

USER_STOP_FLAG = False
FINISHED_CORRECT_FLAG = False
state=0
MAX_STATE=10
lock=threading.Lock()

def update_stop_test_flag(value):
    """
    更新停止测试标志
    :param value: True or False，表示是否停止测试
    """
    global USER_STOP_FLAG
    USER_STOP_FLAG = value

last_time_run_guitest=0
def start_guitest(scene_description):
    """
    启动 GUI 测试流程并管理循环逻辑
    :param json_data: 界面组件的 JSON 数据
    :param scene_description: 测试场景描述
    """
    global USER_STOP_FLAG, state, last_time_run_guitest, val, result, operations
    while time.time() < last_time_run_guitest+10:
        sleep(1)

    if not USER_STOP_FLAG:
        with lock:
            state=0
        print("Capturing current screenshot...")
        capture_screenshot()

    if not USER_STOP_FLAG:
        with lock:
            state=1
        print("Extracting UI components...")
        extract_components()

    if not USER_STOP_FLAG:
        with lock:
            state=2
        print("Generating test operations...")
        json_data = read_json_file()
        operations = generate_test_operations(json_data, scene_description)

    if not USER_STOP_FLAG:
        with lock:
            state=3
        print("Executing test operations...")
        execute_adb_commands(operations)

    if not USER_STOP_FLAG:
        with lock:
            state=4
        print("Re-capturing screenshot and validating state...")
        capture_screenshot()

    if not USER_STOP_FLAG:
        with lock:
            state=5
        extract_components()

    if not USER_STOP_FLAG:
        with lock:
            state=6
        json_data = read_json_file()
        result = generate_test_operations(json_data, scene_description)

    if not USER_STOP_FLAG:
        with lock:
            state=7
        val = validate_operations(result)

    if not USER_STOP_FLAG:
        with lock:
            state=MAX_STATE
        global FINISHED_CORRECT_FLAG
        if val:
            print("Test successful, ending test process")
            FINISHED_CORRECT_FLAG = True
            return True
        elif val is False:
            FINISHED_CORRECT_FLAG = False
            print("Test failed, attempting to correct operations...")
            correcting_prompt="My operation failed. Please help me regenerate the operation to achieve the goal mentioned earlier based on the current interface.For example, after entering the phone number for login, it may have redirected to the password input page. Now, I need to enter the password 'shenfang03' into the input field."
            return start_guitest(correcting_prompt)
        else:
            FINISHED_CORRECT_FLAG = False
            print("Unknown error occurred, ending test process")
        last_time_run_guitest=time.time()
        return True

    if USER_STOP_FLAG:
        print("Ending test process due to user request.")
        FINISHED_CORRECT_FLAG = False
        last_time_run_guitest=time.time()
        return False
