from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .utils.llm_api import analyze_scenario, generate_test_operations
from .utils.screenshot_tools import process_screenshot
from .utils.gui_executor import execute_gui_action
from .utils.state_validator import validate_state

# 上传测试场景
def upload_scenario(request):
    if request.method == "POST":
        scenario_description = request.POST.get("scenario_description", "")
        scenario_state = analyze_scenario(scenario_description)
        return JsonResponse({"status": "success", "message": "场景描述上传成功", "scenario_state": scenario_state})
    return JsonResponse({"status": "error", "message": "仅支持 POST 请求"})

# 启动测试
def start_test(request):
    if request.method == "POST":
        scenario_id = request.POST.get("scenario_id", "")
        # 模拟启动测试逻辑
        return JsonResponse({"status": "started", "message": "测试已启动", "test_id": "67890"})
    return JsonResponse({"status": "error", "message": "仅支持 POST 请求"})

# 查询测试状态
def test_status(request):
    test_id = request.GET.get("test_id", "")
    # 模拟状态查询逻辑
    return JsonResponse({"status": "running", "progress": 75, "current_step": "执行登录按钮点击操作"})

# 获取测试结果
def test_result(request):
    test_id = request.GET.get("test_id", "")
    # 模拟结果返回逻辑
    return JsonResponse({
        "status": "completed",
        "result": "success",
        "logs": ["测试完成", "所有操作符合预期"],
        "screenshots": ["/media/screenshots/step1.png", "/media/screenshots/step2.png"]
    })

# 上传截图
def upload_screenshot(request):
    if request.method == "POST" and request.FILES.get("screenshot"):
        screenshot = request.FILES["screenshot"]
        # 保存文件
        image_path = f"/media/screenshots/{screenshot.name}"
        with open(image_path, "wb") as f:
            for chunk in screenshot.chunks():
                f.write(chunk)
        return JsonResponse({"status": "success", "message": "截图上传成功", "image_path": image_path})
    return JsonResponse({"status": "error", "message": "请上传截图"})

# 获取截图分析结果
def screenshot_analysis(request):
    image_path = request.GET.get("image_path", "")
    analysis_result = process_screenshot(image_path)
    return JsonResponse({"status": "success", "analysis_result": analysis_result})
