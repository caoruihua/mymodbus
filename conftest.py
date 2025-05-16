import pytest
import logging
from config import *
from pymodbus.client import ModbusTcpClient
from Common.FileDataDriver import FileDataDriver
from Common.feishu_test_case import FeishuTestCase

# 自动调起这个文件，代表这个方法即是生效的。所以别的方法可以直接进行调用就可以获取这个数据
# 维护一些前置的方法，必须在main_run.py 文件运行才生效
# 运行的作用范围：默认是 function
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # 通过 out = yield 定义了一个生成器。在生成器中，res = out.get_result() 获取了测试结果对象。
    out = yield
    res = out.get_result()
    #  res.when == "call"：表示正在运行调用测试函数的阶段。
    if res.when == "call":
        logging.info(f"用例ID：{res.nodeid}")
        logging.info(f"测试结果：{res.outcome}")
        logging.info(f"故障表示：{res.longrepr}")
        logging.info(f"异常：{call.excinfo}")
        logging.info(f"用例耗时：{res.duration}")
        logging.info("**************************************")

@pytest.fixture(scope="function")
def register_params_from_excel():
    """读取 Excel 文件中的寄存器参数，包括写入参数。"""
    excel_file = CASEDATAURL
    try:
        # 从excel获取数据
        # data_list = FileDataDriver.readExcel(excel_file)

        # 从飞书获取数据
        data_list = FeishuTestCase(app_id, app_secret, app_token, table_id).get_bitable_data()

        # 如果 data_list 已经是列表格式的记录，直接使用
        return data_list  # 或者根据需要进行其他处理
    except FileNotFoundError:
        pytest.fail(f"Excel 文件未找到: {excel_file}")
    except Exception as e:
        pytest.fail(f"读取 Excel 文件时发生错误: {e}")

@pytest.fixture(scope="function")
def modbus_client(register_params_from_excel):
    """设置和清理 Modbus TCP 客户端连接，并在连接后执行写入操作。"""
    clients = {}
    for params in register_params_from_excel:

        ip = params.get(str("ip"))
        port = params.get("port")
        function_code = params.get("function_code")
        count = params.get("count")
        key = (ip, port)
        # print(key)
        # print(function_code)
        # print(count)
        if key not in clients:
            try:
                client = ModbusTcpClient(ip, port=port)
                if client.connect():
                    clients[key] = client
                    print("mdbus服务链接成功了")
                else:
                    print(f"无法连接到 Modbus 服务器: {ip}:{port}")
            except Exception as e:
                print(f"创建 Modbus 客户端时发生错误: {ip}:{port}: {e}")

    # 在连接建立后执行写入操作
    for params in register_params_from_excel:
        ip = params.get("ip")
        address = int(params.get("address"))
        slave = int(params.get("slave"))  # 默认从站 ID
        port = params.get("port")
        write_value = params.get("write_value")
        write_function_code = params.get("function_code")

        client = clients.get((ip, port))
        if client and write_value is not None and write_function_code is not None:
            print(f"尝试写入到 IP: {ip}, 地址: {address}, SlaveID: {slave}, 端口: {port}, 写入功能码: {write_function_code}, 写入值: {write_value}")
            try:
                if int(count) == 1:
                    if int(function_code) in [1, 2]:
                        result = client.write_coil(address, bool(write_value), slave=slave)  # 写入布尔值，对照功能码02
                    elif int(function_code) in [3, 4]:
                        result = client.write_register(address, int(write_value),slave=slave)  # 写入int或float单个值，对照功能码03、04
                elif int(count) == 2:
                    result = client.write_registers(address, [int(v) for v in write_value],slave=slave)  # 写入int或float多个值，对照功能码03、04
                else:
                    print(f"不支持的写入功能码: {function_code}")
                    continue

                if hasattr(result, 'isError') and result.isError():
                    print(f"写入 Modbus 时发生错误: {result}")
                else:
                    print(f"成功写入 Modbus。")

            except Exception as e:
                print(f"Modbus 写入操作期间发生错误: {e}")

    yield clients

    # 清理：关闭所有连接
    for client in clients.values():
        client.close()



