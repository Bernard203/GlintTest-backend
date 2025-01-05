import time
from .llm_api import generate_test_operations, read_json_file
from .state_validator import validate_operations
from .gui_executor import execute_adb_commands
from .screenshot_tools import capture_screenshot, extract_components

STOP_TEST_FLAG = False
FINISH_TEST_FLAG = False


def update_stop_test_flag(value):
    """
    更新停止测试标志
    :param value: True or False，表示是否停止测试
    """
    global STOP_TEST_FLAG
    STOP_TEST_FLAG = value


def start_guitest(scene_description):
    """
    启动 GUI 测试流程并管理循环逻辑
    :param json_data: 界面组件的 JSON 数据
    :param scene_description: 测试场景描述
    """
    global STOP_TEST_FLAG

    while not STOP_TEST_FLAG:
        print("Capturing current screenshot...")
        capture_screenshot()
        print("Extracting UI components...")
        extract_components()
        json_data = read_json_file()
        print("Generating test operations...")
        operations = generate_test_operations(json_data, scene_description)
        print("Executing test operations...")
        execute_adb_commands(operations)

        print("Re-capturing screenshot and validating state...")
        capture_screenshot()
        extract_components()
        json_data = read_json_file()

        result = generate_test_operations(json_data, scene_description)
        val = validate_operations(result)
        global FINISH_TEST_FLAG
        if val:
            print("Test successful, ending test process")
            FINISH_TEST_FLAG = True
            return True
        elif val is False:
            FINISH_TEST_FLAG = False
            print("Test failed, attempting to correct operations...")
        else:
            FINISH_TEST_FLAG = False
            print("Unknown error occurred, ending test process")
        # 等待一段时间（避免快速重复调用）
        time.sleep(5)

    print("Ending test process due to user request.")
    FINISH_TEST_FLAG = False
    return False
