import logging
import pytest
import allure
from config import *
from Common.feishu_test_case import FeishuTestCase
from Common.modbus_value import ProcessModbusData
from Common.sql_value import ProcessMongodbData

# 初始化日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
db_logger = logging.getLogger("database")
modbus_logger = logging.getLogger("modbus")


def dynamic_title(test_data):
    """动态生成allure报告标题"""
    allure.dynamic.title(test_data["Title"])

    # 如果存在自定义标题
    if test_data["Title"] is not None:
        # 动态生成标题
        allure.dynamic.title(test_data["Title"])

    # if test_data["storyName"] is not None:
    #     # 动态获取story模块名
    #     allure.dynamic.story(test_data["storyName"])

    # if test_data["featureName"] is not None:
    #     # 动态获取feature模块名
    #     allure.dynamic.feature(test_data["featureName"])
    #
    # if test_data["remark"] is not None:
    #     # 动态获取备注信息
    #     allure.dynamic.description(test_data["remark"])
    #
    # if test_data["rank"] is not None:
    #     # 动态获取级别信息(blocker、critical、normal、minor、trivial)
    #     allure.dynamic.severity(test_data["rank"])
# 获取飞书数据
def test_data():
    global feishu_test_case
    feishu_test_case = FeishuTestCase(APP_ID, APP_SECRET, APP_TOKEN, TABLE_ID)
    feishu_case_data = feishu_test_case.get_bitable_data()
    return feishu_case_data

@pytest.mark.parametrize("test_data", test_data())
def test_modbus_and_mongodb(test_data):

    # 测试逻辑
    ip = test_data.get("ip")
    port = test_data.get("port")
    address = int(test_data.get("address"))
    count = test_data.get("count")
    slave = test_data.get("slave")
    function_code = test_data.get("function_code")
    write_value = test_data.get("write_value")
    datatype = test_data.get("datatype")
    dataformat = test_data.get("dataformat")
    query_params = test_data.get("query_params")
    collection = test_data.get("collection")
    expected_result = test_data.get("Expected_result")
    record_id = test_data.get("record_id")
    dynamic_title(test_data)
    try:
        # 写入modbus数据
        modbus_data = ProcessModbusData(ip, port, address, count, slave, function_code, write_value, datatype, dataformat).write_modbus_register()
        modbus_logger.info(f"Modbus 数据: {modbus_data}")
    except Exception as e:
        modbus_logger.error(f"Modbus 数据写入失败: {e}")
        pytest.fail("Modbus 数据写入失败")

    try:
        # 获取mongodb数据
        mg_data = ProcessMongodbData().get_mongodb_value(query_params, collection)
        print(f"mg_data: {mg_data}")
        db_logger.info(f"MongoDB 数据: {mg_data}")
        # mongodb获取结果更新到飞书
        feishu_test_case.updata_bitable_data(record_id, "Mongomysqlresult", mg_data)
        db_logger.info(f"MongoDB 数据写入成功: {mg_data}")
        print(f"预期结果：{expected_result}，mongo提取结果{mg_data}")
        print(type(expected_result))
        print(type(mg_data))
    except Exception as e:
        db_logger.error(f"MongoDB 数据获取失败: {e}")
        pytest.fail("MongoDB 数据获取失败")

    if float(expected_result) == float(mg_data):

        feishu_test_case.updata_bitable_data(record_id, "checkResult", "成功")
    else:
        feishu_test_case.updata_bitable_data(record_id, "checkResult", "失败")

    assert float(mg_data) == float(expected_result)