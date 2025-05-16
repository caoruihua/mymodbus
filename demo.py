from pymodbus.client import ModbusTcpClient
from sqlalchemy.sql.operators import truediv


def modbus_client(ip,port,address,slave,write_value,function_code,count):
    clients = {}
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

    if client and write_value is not None and function_code is not None:
        print(f"尝试写入到 IP: {ip}, 地址: {address}, 从站: {slave}, 端口: {port}, 写入功能码: {function_code}, 写入值: {write_value}")
        try:
            if count == 1:
                if function_code in [1, 2]:
                    result = client.write_coil(address, bool(write_value), slave=slave)  # 写入布尔值，对照功能码02
                elif function_code in [3, 4]:
                    result = client.write_register(address, int(write_value),slave=slave)  # 写入int或float单个值，对照功能码03、04
            elif count == 2:
                result = client.write_registers(address, [int(v) for v in write_value],slave=slave)  # 写入int或float多个值，对照功能码03、04
            else:
                print(f"不支持的写入功能码: {function_code}")
                pass

            if hasattr(result, 'isError') and result.isError():
                print(f"写入 Modbus 时发生错误: {result}")
            else:
                print(f"成功写入 Modbus。")

        except Exception as e:
            print(f"Modbus 写入操作期间发生错误: {e}")

    # 清理：关闭所有连接
    client.close()
if __name__ == '__main__':
    modbus_client('127.0.0.1',602,32,1,12,4,1)