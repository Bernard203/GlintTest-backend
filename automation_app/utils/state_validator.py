import json


def validate_operations(json_data, scene_description):
    """
    根据生成的 JSON 数据和目标场景验证测试是否成功。

    :param json_data: 当前界面状态
    :param scene_description: 目标场景描述
    :return: 验证结果
    """
    print("Validating operations...")
    # 示例逻辑：检查界面是否包含目标文本
    for component in json_data.get("components", []):
        if scene_description in component.get("ocr_text", ""):
            return True, "Validation passed."
    return False, "Validation failed. Target text not found."
