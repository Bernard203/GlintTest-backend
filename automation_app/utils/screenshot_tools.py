import subprocess
import os
import cv2
import pytesseract
import os
import numpy as np
import json
from matplotlib import pyplot as plt
from .wid_analysis import get_classfication

import subprocess
from PIL import Image
import os

SCREENSHOT_DIR = '../screenshots'

def capture_screenshot():
    target_folder = SCREENSHOT_DIR
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    existing_files = os.listdir(target_folder)
    screenshot_count = len([f for f in existing_files if f.endswith('.png')])

    screenshot_name = f"{screenshot_count + 1}.png"
    screenshot_path = os.path.join(target_folder, screenshot_name)

    with open(screenshot_path, 'wb') as f:
        subprocess.run(['adb', 'exec-out', 'screencap', '-p'], stdout=f)

    print(f"Screenshot saved as {screenshot_path}")
    return screenshot_path

class Bbox:
    def __init__(self, x1, y1, x2, y2, category, ocr_text=None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.category = category  # 分类结果
        self.ocr_text = ocr_text  # OCR提取的文本

    def get_coordinates(self):
        return self.x1, self.y1, self.x2, self.y2

    def get_center(self):
        # 计算中心点坐标
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return center_x, center_y

    def get_size(self):
        # 计算宽和高
        width = self.x2 - self.x1
        height = self.y2 - self.y1
        return width, height


# 将边界框信息保存为JSON文件
def save_bboxs_as_json(bboxs, save_path):
    res = {'components': []}
    for b in bboxs:
        x1, y1, x2, y2 = b.get_coordinates()
        center_x, center_y = b.get_center()
        width, height = b.get_size()
        category = b.category
        ocr_text = b.ocr_text

        res['components'].append({
            'category': category,
            'ocr_text': ocr_text,
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'center': {'x': center_x, 'y': center_y},
            'size': {'width': width, 'height': height}
        })

    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=4)


# 获取最新的截图文件路径（最大编号）
def get_latest_screenshot(screenshot_dir=SCREENSHOT_DIR):
    # 获取文件夹中所有的PNG文件
    existing_files = os.listdir(screenshot_dir)
    # 过滤出所有PNG文件
    png_files = [f for f in existing_files if f.endswith('.png')]

    # 如果没有截图文件，返回None
    if not png_files:
        return None

    # 获取文件名中的数字部分并找出最大值
    latest_file = max(png_files, key=lambda f: int(f.split('.')[0]))

    # 返回最新的截图文件路径
    return os.path.join(screenshot_dir, latest_file)


# 提取图像中的文本
def extract_text_from_image(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray_image, config='--psm 6')
    return text.strip()


# 在图像上绘制边界框并保存
def draw_rectangle_show_save(image, bboxes, output_path):
    for bbox in bboxes:
        x1, y1, x2, y2 = bbox.get_coordinates()
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.imwrite(output_path, image)


# 提取组件并保存图像
def save_component_images(image, contours, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    components_info = []
    bboxs = []

    for idx, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        component_image = image[y:y + h, x:x + w]
        ocr_text = extract_text_from_image(component_image)
        category = get_classfication(component_image)


        bbox = Bbox(x, y, x + w, y + h, category, ocr_text)
        bboxs.append(bbox)

        components_info.append({
            'bbox': bbox,
            'category': category,
            'ocr_text': ocr_text
        })

    json_save_path = os.path.join(output_dir, "components.json")
    save_bboxs_as_json(bboxs, json_save_path)

    return components_info

def flood_fill_edges(canny_image):
    """
    在 Canny 边缘检测结果上进行膨胀操作并合并。
    """
    # 对边缘进行膨胀操作，增强连接
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 小的矩形核
    dilated = cv2.dilate(canny_image, kernel, iterations=3)  # 膨胀操作

    combined = cv2.bitwise_or(canny_image, dilated)  # 按位或操作合并

    return combined



def extract_components():
    image_path = get_latest_screenshot()
    output_dir = './output'
    image = cv2.imread(image_path)
    print(image.shape)

    # 转为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 高斯模糊
    # blurred_image = cv2.GaussianBlur(gray_image, (11, 11), 0)
    # cv2.imwrite(os.path.join(output_dir, "blurred_image.png"), blurred_image)
    # print("高斯模糊图已保存：blurred_image.png")

    # Canny边缘检测
    edges_image = cv2.Canny(gray_image, 100, 200)
    cv2.imwrite(os.path.join(output_dir, "edges_image.png"), edges_image)
    print("Canny边缘检测结果已保存：edges_image.png")

    # 在Canny边缘图像上应用泛洪操作，增强边缘连接
    flood_filled_edges = flood_fill_edges(edges_image)
    cv2.imwrite(os.path.join(output_dir, "flood_filled_edges.png"), flood_filled_edges)
    print("泛洪操作后的图像已保存")

    # 找到轮廓
    contours, _ = cv2.findContours(flood_filled_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 保存并分类组件
    components_info = save_component_images(image, contours, output_dir)

    # 绘制边界框并保存最终图像
    draw_rectangle_show_save(image, [info['bbox'] for info in components_info], os.path.join(output_dir, "output_image_with_bbox.png"))
    print("最终结果图像已保存")