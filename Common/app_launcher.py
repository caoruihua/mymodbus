import pywinauto
import logging
from config import *  # 假设 config.py 中定义了 app_path 和其他配置参数


def launch_desktop_application():
    try:
        # 创建应用实例
        app = pywinauto.Application(APP_PATH)
        print("正在尝试启动应用：", APP_PATH)

        # 设置启动选项
        options = {
            'backend': BACKEND,
            'wait': WINDOW_TITLE,
            'timeout': TIMEOUT,
            'run_as_admin': True  # 启动时以管理员身份运行
        }

        # 启动应用程序
        result = app.start(**options)

        if not result:
            raise Exception("无法启动指定的 Windows 应用程序")

        return True

    except Exception as e:
        # print(f"启动 Windows 桌面应用失败：{str(e)}")
        pywinauto.WindowNotFoundError = 'Traceback'
        logging.error(f"错误信息：{str(e)}")


        return False
if __name__ == "__main__":
    launch_desktop_application()