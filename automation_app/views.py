from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.core.cache import cache
from .utils.llm_api import generate_test_operations, read_json_file
from .utils.run_test import start_guitest
from .utils.screenshot_tools import capture_screenshot
from .utils.gui_executor import execute_adb_commands
from .utils.state_validator import validate_operations

scene_description = "Test the login function of the app."

# 上传测试场景
def upload_scenario(request):
    if request.method == "POST":
        scene_description = request.POST.get("scene_description")
        if scene_description:
            cache.set("scene_description", scene_description, timeout=3600)  # Cache for 1 hour
            return JsonResponse({"message": "Scene description cached successfully"})
        return JsonResponse({"error": "Scene description is required"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=400)


# 启动测试
def start_test(request):
    if request.method == "POST":
        scene_description = cache.get("scene_description")
        if not scene_description:
            return JsonResponse({"error": "Scene description not found"}, status=400)
        start_guitest(scene_description)
        return JsonResponse({"message": "Test started successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=400)


# 查询测试状态
def test_status(request):
    pass

# 获取测试结果
def test_result(request):
    pass

# 上传截图
def upload_screenshot(request):
    if request.method == "POST":
        screenshot = request.FILES.get("screenshot")
        if screenshot:
            cache.set("screenshot", screenshot, timeout=3600)  # Cache for 1 hour
            return JsonResponse({"message": "Screenshot uploaded successfully"})
        return JsonResponse({"error": "Screenshot file is required"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=400)


# 获取截图分析结果
def screenshot_analysis(request):
    pass