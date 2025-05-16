from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadBuilder
import logging
import struct

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - 模块:modbus_reader - %(message)s',
    handlers=[
        logging.FileHandler('modbus_reader.log'),
        logging.StreamHandler()  # 添加控制台输出
    ]
)
 # 修正了handlers定义

logger = logging.getLogger('modbus_reader')  # 修正了logger名称


class ProcessModbusData:
    # 初始化
    def __init__(self, ip, port, address, count, slave, function_code, write_value, datatype=None, dataformat=None):
        self.ip = ip
        self.port = port
        self.address = address
        self.count = count
        self.slave = slave
        self.function_code = function_code
        self.datatype = datatype
        self.dataformat = dataformat
        self.write_value = write_value
        """
            统一的Modbus寄存器读取函数
    
            :param ip: Modbus服务器IP
            :param port: Modbus服务器端口
            :param address: 寄存器地址
            :param count: 读取数量
            :param slave: 从站ID
            :param function_code: 功能码(1=线圈, 2=离散输入, 3=保持寄存器, 4=输入寄存器)
            :param datatype: 数据类型(1=long, 2=float)，仅用于功能码3和4
            :param dataformat: 字节序(1=前高后低, 2=前低后高)，仅用于功能码3和4
            :return: 读取的数据
        """
        # 连接modbus
        self.client = ModbusTcpClient(host=ip, port=port, timeout=3000)

    # 连接信息
    def connect(self):
        if self.client():
            logger.info("成功连接到 Modbus 服务器")
        else:
            logger.error("连接失败")
            exit(1)

    # 写入寄存器数据
    def write_modbus_register(self):
        if self.client and self.write_value is not None and self.function_code is not None:
            print(f"尝试写入到 IP: {self.ip}, 地址: {self.address}, SlaveID: {self.slave}, 端口: {self.port}, 写入功能码: {self.function_code}, 写入值: {self.write_value}")
            try:
                if int(self.count) == 1:
                    if int(self.function_code) in [1, 2]:
                        result = self.client.write_coil(self.address, bool(self.write_value), slave=self.slave)  # 写入布尔值，对照功能码02
                    elif int(self.function_code) in [3, 4]:
                        result = self.client.write_register(self.address, int(self.write_value), slave=self.slave)  # 写入int或float单个值，对照功能码03、04
                # 高低位处理
                elif int(self.count) == 2:
                    # 前高后低
                    if self.dataformat == 1:
                        result = self.client.write_registers(self.address, self.write_value, slave=self.slave)
                    elif self.dataformat == 2:
                        self.write_value = self.write_value[::-1]
                        result = self.client.write_registers(self.address, self.write_value, slave=self.slave)

                    # result = self.client.write_registers(self.address, [int(v) for v in self.write_value], slave=self.slave)
                    # result = self.client.write_registers(self.address, self.write_value, slave=self.slave)
                    # 写入int或float多个值，对照功能码03、04
                else:
                    print(f"不支持的写入功能码: {self.function_code}")

                if hasattr(result, 'isError') and result.isError():
                    print(f"写入 Modbus 时发生错误: {result}")
                else:
                    print(f"成功写入 Modbus。")

            except Exception as e:
                print(f"Modbus 写入操作期间发生错误: {e}")

    # @staticmethod
    # def read_modbus_register():
    #     """
    #     统一的Modbus寄存器读取函数
    #
    #     :param ip: Modbus服务器IP
    #     :param port: Modbus服务器端口
    #     :param address: 寄存器地址
    #     :param count: 读取数量
    #     :param slave: 从站ID
    #     :param function_code: 功能码(1=线圈, 2=离散输入, 3=保持寄存器, 4=输入寄存器)
    #     :param datatype: 数据类型(1=long, 2=float)，仅用于功能码3和4
    #     :param dataformat: 字节序(1=前高后低, 2=前低后高)，仅用于功能码3和4
    #     :return: 读取的数据
    #     """
    #     data = self_client.read_input_registers(address, count=count, slave=slave)
    #     print(f"读取结果：{data}")
    #     try:
    #         if not client.connect():
    #             logging.error(f"连接失败: {ip}:{port}")
    #             print("连接失败，无法建立Modbus连接。")
    #             return None
    #
    #         # 根据功能码选择不同的读取方法
    #         function_code = int(function_code)
    #         if function_code == 1:
    #             response = client.read_coils(address=address, count=count, slave=slave)
    #         elif function_code == 2:
    #             response = client.read_discrete_inputs(address=address, count=count, slave=slave)
    #         elif function_code == 3:
    #             response = client.read_holding_registers(address=address, count=count, slave=slave)
    #         elif function_code == 4:
    #             # 使用关键字参数而不是位置参数
    #             response = client.read_input_registers(address=address, count=count, slave=slave)
    #         else:
    #             raise ValueError(f"不支持的功能码: {function_code}")
    #
    #         if response.isError():
    #             logging.error(f"Modbus错误: {response}")
    #             print(f"Modbus 错误: {response}")
    #             return None
    #
    #         # 处理不同类型的返回值
    #         if function_code in [1, 2]:  # 线圈和离散输入
    #             value = response.bits[0]
    #             if function_code == 2:
    #                 print(1 if value else 0)
    #             return value
    #
    #         elif function_code in [3, 4]:  # 寄存器
    #             registers = response.registers
    #
    #             # 单个寄存器的简单情况
    #             if len(registers) == 1 or (datatype is None and count == 1):
    #                 value = registers[0]
    #                 result = round(value, 2) if isinstance(value, float) else value
    #                 print(f"{result}")
    #                 return result
    #
    #             # 处理多寄存器组合的情况
    #             if dataformat == 1:  # 前低后高cd ab
    #                 high_reg = data.registers[0]  # 0x000（高位）
    #                 low_reg = data.registers[1]  # 0x001（低位）
    #             else:  # 前高后低ab cd
    #                 high_reg = data.registers[1]  # 0x000（高位）
    #                 low_reg = data.registers[0]  # 0x001（低位）
    #
    #             if datatype == 1:  # long
    #                 # 这里应该有处理long类型的代码
    #                 value = (high_reg << 16) | low_reg
    #                 return value
    #
    #             elif datatype == 2:  # float
    #                 bytes_data = high_reg.to_bytes(2, 'big') + low_reg.to_bytes(2, 'big')
    #                 value = struct.unpack('>f', bytes_data)[0]  # '>f' 表示大端浮点数
    #                 print(f"{value}")
    #                 return value
    #
    #     except Exception as e:
    #         logging.error(f"读取Modbus寄存器失败，原因：{str(e)}", exc_info=True)
    #         print(f"捕获异常：{e}")
    #         return None
    #     finally:
    #         client.close()


if __name__ == '__main__':
    from TaokeEms.config import *
    from TaokeEms.Common.feishu_test_case import FeishuTestCase
    ProcessModbusData("127.0.0.1", "501", 34, 2, 1, 3, [1, 2], datatype=None, dataformat=2).write_modbus_register()

    # AllCaseData = FeishuTestCase(app_id, app_secret, app_token, table_id).get_bitable_data()[0]
    # ip = AllCaseData["ip"]
    # port = AllCaseData["port"]
    # address = int(AllCaseData["address"])
    # count = AllCaseData["count"]
    # slave = AllCaseData["slave"]
    # function_code = AllCaseData["function_code"]
    # write_value = AllCaseData["write_value"]
    # datatype = AllCaseData["datatype"]
    # dataformat = AllCaseData["dataformat"]
    # print(f"ip{type(ip)}, port{type(port)}, address{type(address)}, count{type(count)}, slave{type(slave)}, "
    #       f"function_code{type(function_code)}, write_value{type(write_value)}, "f"datatype{type(datatype)}, dataformat{type(dataformat)}")
    #
    # modbus_data = ProcessModbusData(ip, port, address, count, slave, function_code, write_value, datatype,
    #                                 dataformat).write_modbus_register()
    #
    # print(modbus_data)
