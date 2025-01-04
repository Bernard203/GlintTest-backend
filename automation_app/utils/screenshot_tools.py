import subprocess
import os
import cv2
import pytesseract


def capture_screenshot(output_dir='./screenshots'):
    """
    截取屏幕并保存为 PNG 文件。

    :param output_dir: 截图保存目录
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    screenshot_count = len([f for f in os.listdir(output_dir) if f.endswith('.png')])
    screenshot_name = f"{screenshot_count + 1}.png"
    screenshot_path = os.path.join(output_dir, screenshot_name)

    with open(screenshot_path, 'wb') as f:
        subprocess.run(['adb', 'exec-out', 'screencap', '-p'], stdout=f)
    print(f"Screenshot saved at {screenshot_path}")
    return screenshot_path


def extract_text(image_path):
    """
    使用 Tesseract OCR 提取图像中的文本。

    :param image_path: 图像路径
    :return: 提取的文本
    """
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray_image, config='--psm 6')
    return text.strip()
