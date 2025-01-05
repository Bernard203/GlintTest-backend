from django.urls import path
from . import views

urlpatterns = [
    path('upload_scenario/', views.upload_scenario, name='upload_scenario'),
    path('start_test/', views.start_test, name='start_test'),
    path('test_status/', views.test_status, name='test_status'),
    path('test_result/', views.test_result, name='test_result'),
    # path('upload_screenshot/', views.upload_screenshot, name='upload_screenshot'),
    # path('screenshot_analysis/', views.screenshot_analysis, name='screenshot_analysis'),
]
