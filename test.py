# 核心依赖库
import tkinter as tk
from tkinter import ttk
from pymodbus.client import ModbusTcpClient
from threading import Thread, Event
import time

class ModbusClientGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Modbus TCP客户端 v1.0")

        # 连接配置区
        config_frame = ttk.LabelFrame(self.window, text="连接配置")
        config_frame.grid(row=0, column=0, padx=10, pady=10)

        ttk.Label(config_frame, text="IP地址:").grid(row=0, column=0)
        self.ip_entry = ttk.Entry(config_frame)
        self.ip_entry.grid(row=0, column=1)

        ttk.Label(config_frame, text="设备单元号:").grid(row=0, column=2)
        self.unit_entry = ttk.Entry(config_frame)
        self.unit_entry.grid(row=0, column=3)

        # 功能码下拉选择
        ttk.Label(config_frame, text="功能码:").grid(row=1, column=0)
        self.func_code = ttk.Combobox(config_frame, values=["03-读保持寄存器", "04-读输入寄存器"])
        self.func_code.current(0)
        self.func_code.grid(row=1, column=1)

        ttk.Label(config_frame, text="起始地址:").grid(row=1, column=2)
        self.addr_entry = ttk.Entry(config_frame)
        self.addr_entry.grid(row=1, column=3)

        ttk.Label(config_frame, text="寄存器数量:").grid(row=2, column=0)
        self.reg_count = ttk.Entry(config_frame)
        self.reg_count.grid(row=2, column=1)
        self.reg_count.insert(0, "1")  # 默认值为1

        # 轮询时间配置
        ttk.Label(config_frame, text="轮询间隔(ms):").grid(row=2, column=2)
        self.interval = ttk.Spinbox(config_frame, from_=100, to=5000, increment=100)
        self.interval.set(1000)
        self.interval.grid(row=2, column=3)

        # 数据显示区
        self.data_text = tk.Text(self.window, height=15)
        self.data_text.grid(row=1, column=0, padx=10, pady=10)

        # 控制按钮
        button_frame = ttk.Frame(self.window)
        button_frame.grid(row=2, column=0, padx=10, pady=10)

        self.start_btn = ttk.Button(button_frame, text="启动轮询", command=self.start_polling)
        self.start_btn.grid(row=0, column=0, padx=5)

        self.stop_btn = ttk.Button(button_frame, text="停止轮询", command=self.stop_polling)
        self.stop_btn.grid(row=0, column=1, padx=5)

        # 初始化轮询控制器
        self.polling_controller = None

    def start_polling(self):
        if self.polling_controller is None:
            self.polling_controller = PollingController(self)
        self.polling_controller.start_polling()

    def stop_polling(self):
        if self.polling_controller:
            self.polling_controller.stop_polling()
            self.polling_controller = None


class ModbusHandler:
    FUNCTION_MAP = {
        3: 'read_holding_registers',
        4: 'read_input_registers'
    }

    def __init__(self, ip, port=502, unit=1):
        self.client = ModbusTcpClient(host=ip, port=port)
        self.unit = unit
        self.is_connected = False

    def connect(self):
        try:
            self.is_connected = self.client.connect()
            return self.is_connected
        except Exception as e:
            print(f"连接失败: {str(e)}")
            return False

    def read_data(self, func_code, address, count):
        if func_code not in self.FUNCTION_MAP:
            raise ValueError("不支持的功能码")

        method = getattr(self.client, self.FUNCTION_MAP[func_code])
        return method(address=address, count=count, slave=self.unit)


class PollingController:
    def __init__(self, gui):
        self.gui = gui
        self.polling_thread = None
        self.stop_event = Event()

    def start_polling(self):
        # 初始化Modbus连接
        ip = self.gui.ip_entry.get()
        unit = int(self.gui.unit_entry.get())
        self.modbus = ModbusHandler(ip=ip, unit=unit)
        if not self.modbus.connect():
            self.gui.data_text.insert(tk.END, f"[ERROR] 无法连接到 {ip}\n")
            return

        # 启动轮询线程
        self.polling_thread = Thread(target=self._polling_loop)
        self.polling_thread.start()

    def stop_polling(self):
        self.stop_event.set()
        if self.polling_thread:
            self.polling_thread.join()

    def _polling_loop(self):
        while not self.stop_event.is_set():
            start_time = time.time()

            # 执行读取操作
            try:
                func_code = int(self.gui.func_code.get().split('-')[0])
                address = int(self.gui.addr_entry.get())
                count = int(self.gui.reg_count.get())

                response = self.modbus.read_data(func_code, address, count)

                # 更新界面数据
                self.gui.data_text.insert(tk.END,
                                          f"[{time.strftime('%H:%M:%S')}] 寄存器值: {response.registers}\n")

            except Exception as e:
                self.gui.data_text.insert(tk.END,
                                          f"[ERROR] {str(e)}\n")

            # 控制轮询间隔
            elapsed = (time.time() - start_time) * 1000
            sleep_time = max(0, int(self.gui.interval.get()) - elapsed)
            time.sleep(sleep_time / 1000)


if __name__ == '__main__':
    modbus_gui = ModbusClientGUI()
    modbus_gui.window.mainloop()

