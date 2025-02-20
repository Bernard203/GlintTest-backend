from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.core.cache import cache
from .utils.run_test import start_guitest, MAX_STATE
import threading

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
        threading.Thread(target=start_guitest, args=(scene_description,), daemon=True).start()
        return JsonResponse({"message": "Test started successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=400)

# 查询测试状态
def test_status(request):
    if request.method == "GET":
        from .utils.run_test import state
        if state==MAX_STATE:
            return JsonResponse({"message": "Test finished."})
        else:
            return JsonResponse({"message": "Test in progress."})
    return JsonResponse({"error": "Invalid request method"}, status=400)

# 获取测试结果
def test_result(request):
    if request.method == "GET":
        from .utils.run_test import FINISHED_CORRECT_FLAG
        if FINISHED_CORRECT_FLAG:
            return JsonResponse({"message": "Test successful, ending test process."})
        else:
            return JsonResponse({"message": "Test failed."})
    return JsonResponse({"error": "Invalid request method"}, status=400)