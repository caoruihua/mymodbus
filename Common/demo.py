import pytest
from pymodbus.client import ModbusTcpClient
from FileDataDriver import FileDataDriver
from TaokeEms.config import *
from feishu_test_case import GetFeishuTestCase

class DOME:
    def register_params_from_excel(self):
        """读取 Excel 文件中的寄存器参数，包括写入参数。"""
        excel_file = CASEDATAURL
        try:
            # df = FileDataDriver.readExcel(excel_file)
            df = GetFeishuTestCase
            # 假设你的 Excel 文件包含以下列名：ip, address, slave, port, function_code, write_value, write_function_code
            params = df.to_dict(orient="records")
            return params
        except FileNotFoundError:
            pytest.fail(f"Excel 文件未找到: {excel_file}")
        except Exception as e:
            pytest.fail(f"读取 Excel 文件时发生错误: {e}")
    # @pytest.fixture
    def modbus_client(ip, port,address,function_code,count,slave,write_value):
        """设置和清理 Modbus TCP 客户端连接，并在连接后执行写入操作。"""
        client = ModbusTcpClient(host=ip, port=port, timeout=3000)

        # 在连接建立后执行写入操作
        if client and write_value is not None and function_code is not None:
            print(f"尝试写入到 IP: {ip}, 地址: {address}, 从站: {slave}, 端口: {port}, 写入功能码: {function_code}, 写入值: {write_value}")
            try:
                if count == 1 :  # 写单个/多个线圈
                    if function_code in [1,2]:
                        #写入布尔值，对照功能码02
                        data_value = bool(write_value) if isinstance(write_value, int) else write_value
                        client.write_coil(address, data_value)
                    elif function_code in [3,4]:
                        result = client.write_register(address, int(write_value), slave=slave) #写入int或float单个值，对照功能码03、04
                elif count == 2 :  # 写单个/多个保持寄存器
                    result = client.write_registers(address, [int(v) for v in write_value], slave=slave)#写入int或float多个值，对照功能码03、04

                else:
                    print(f"不支持的写入功能码: {function_code}")


                if hasattr(result, 'isError') and result.isError():
                    print(f"写入 Modbus 时发生错误: {result}")
                else:
                    print(f"成功写入 Modbus。")

            except Exception as e:
                print(f"Modbus 写入操作期间发生错误: {e}")


            finally:

                # 确保总是关闭客户端连接
                if modbus_client is not None:
                    modbus_client.close()

if __name__ == '__main__':
    DOME.register_params_from_excel()
    # modbus_client('127.0.0.1',601,1,2,1,1,1)
