import subprocess
import time


def execute_adb_commands(operations, delay=2):
    """
    执行 ADB 命令列表，并在每个命令之间设置延迟。

    :param operations: 包含多个 ADB 命令的字符串
    :param delay: 每条命令之间的延迟时间，默认 2 秒
    """
    if not operations:
        print("No operations to execute.")
        return

    commands = operations.splitlines()
    for command in commands:
        if command.strip():
            try:
                print(f"Executing: {command}")
                subprocess.run(command, shell=True, check=True)
                time.sleep(delay)
            except subprocess.CalledProcessError as e:
                print(f"Failed to execute command: {command}\nError: {e}")


def tap_screen(x, y):
    """
    模拟屏幕点击操作。

    :param x: 点击的 x 坐标
    :param y: 点击的 y 坐标
    """
    adb_command = f"adb shell input tap {x} {y}"
    execute_adb_commands(adb_command)


def input_text(text):
    """
    模拟文本输入操作。

    :param text: 要输入的文本
    """
    adb_command = f"adb shell input text '{text}'"
    execute_adb_commands(adb_command)


def swipe_screen(x1, y1, x2, y2):
    """
    模拟屏幕滑动操作。

    :param x1: 滑动起点 x 坐标
    :param y1: 滑动起点 y 坐标
    :param x2: 滑动终点 x 坐标
    :param y2: 滑动终点 y 坐标
    """
    adb_command = f"adb shell input swipe {x1} {y1} {x2} {y2}"
    execute_adb_commands(adb_command)
