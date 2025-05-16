from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

# 创建 Modbus 客户端
client = ModbusTcpClient('127.0.0.1', port=501)  # 替换为你的 Modbus 服务器地址和端口

# 连接到 Modbus 服务器
client.connect()

# 要写入的 32 位整数
value_to_write = 0x12345678  # 示例值

# 创建构建器
builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)

# 将 32 位整数拆分为两个 16 位寄存器
builder.add_32bit_uint(value_to_write)

# 获取寄存器值
registers = builder.to_registers()

# 写入寄存器
client.write_registers(address=34, values=registers, unit=1)  # address 是起始寄存器地址，unit 是从站地址

# 读取寄存器以验证写入
result = client.read_holding_registers(address=34, count=2, unit=1)

# 解码读取的值
decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)
decoded_value = decoder.decode_32bit_uint()

print(f"写入的值: {value_to_write}")
print(f"读取的值: {decoded_value}")

# 断开连接
client.close()