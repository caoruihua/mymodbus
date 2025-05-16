from pandas.io.formats.format import return_docstring

from TaokeEms.Common.sql_value import ProcessMongodbData
from TaokeEms.Common.modbus_value import ProcessModbusData
# from Common.FileDataDriver import FileDataDriver
from TaokeEms.Common.feishu_test_case import FeishuTestCase
# from Common.Modbus_value import READMODBUS
from TaokeEms.config import *
import logging
import pytest
import allure
import ast



# 初始化领域日志记录器
db_logger = logging.getLogger("database")
modbus_logger = logging.getLogger("modbus")

@pytest.fixture(scope="module")
def test_data():
    # 从excel获取测试数据
    # AllCaseData = FileDataDriver.readExcel()  #数据源

    # 从飞书获取测试数据
    feishu_test_case = FeishuTestCase(app_id, app_secret, app_token, table_id) # 数据源
    all_case_data = feishu_test_case.get_bitable_data()
    return all_case_data

# 参数化
@pytest.mark.parametrize("case_data", test_data(), indirect=True)
def test_modbus_and_mongodb(case_data):
    ip = case_data["ip"]
    port = case_data["port"]
    address = int(case_data["address"])
    count = case_data["count"]
    slave = case_data["slave"]
    function_code = case_data["function_code"]
    write_value = case_data["write_value"]
    datatype = case_data["datatype"]
    dataformat = case_data["dataformat"]
    query_params = case_data["query_params"]
    collection = case_data["collection"]

    # 写入modbus
    modbus_data = ProcessModbusData(ip, port, address, count, slave, function_code, write_value, datatype, dataformat).write_modbus_register()
    modbus_logger.info(f"Modbus 数据: {modbus_data}")

    # 获取mongodb数据
    mg_data = ProcessMongodbData().get_mongodb_value(query_params, collection)
    db_logger.info(f"MongoDB 数据: {mg_data}")

    # 断言
    assert modbus_data == mg_data, "Modbus 数据与 MongoDB 数据不一致"
    # sq = GETSQLVALUE() #实例化sql提取类
    # modb = READMODBUS()  #实例化modbus数据提取类
    # all_var = {}  # 存放所有的公共全局变量



    # def dynamic_title(self, CaseData):
    #     """动态生成allure报告标题"""
    #     # allure.dynamic.title(data[2])
    #     # 如果存在自定义标题
    #     if CaseData["caseName"] is not None:
    #         # 动态生成标题
    #         allure.dynamic.title(CaseData["caseName"])
    #
    #     if CaseData["storyName"] is not None:
    #         # 动态获取story模块名
    #         allure.dynamic.story(CaseData["storyName"])
    #
    #     # if CaseData["featureName"] is not None:
    #     #     # 动态获取feature模块名
    #     #     allure.dynamic.feature(CaseData["featureName"])
    #
    #     if CaseData["remark"] is not None:
    #         # 动态获取备注信息
    #         allure.dynamic.description(CaseData["remark"])
    #
    #     if CaseData["rank"] is not None:
    #         # 动态获取级别信息(blocker、critical、normal、minor、trivial)
    #         allure.dynamic.severity(CaseData["rank"])


    # def __mysql_mongodb_extraction(self, CaseData):
    #     """处理数据库操作并返回结果"""
    #     try:
    #         # 优先处理MongoDB
    #         db_logger.debug("开始数据库操作")
    #         if CaseData.get("query_params") and CaseData.get("collection"):
    #             db_logger.info(f"MongoDB查询参数: {CaseData['query_params']}")
    #             # 安全解析查询参数
    #             query_params = ast.literal_eval(CaseData["query_params"])
    #
    #             # 获取独立collection字段
    #             collection_name = ast.literal_eval(CaseData["collection"]).strip()
    #             if not collection_name:
    #                 raise ValueError("MongoDB collection不能为空")
    #             return self.sq.get_mongodb_value(
    #                 query_params=query_params,
    #                 collection=collection_name
    #             )
    #
    #
    #         # 处理MySQL
    #         elif CaseData.get("sqlExData"):
    #             sql = eval(CaseData["sqlExData"]).strip()
    #             if not sql:
    #                 raise ValueError("SQL语句不能为空")
    #             return self.sq.get_mysql_value(sql)
    #         return "NO_DB_OPERATION"
    #
    #     except SyntaxError as e:
    #         db_logger.error("数据库操作异常", exc_info=True)
    #         return f"语法错误: {str(e)}"
    #     except Exception as e:
    #         return f"数据库错误: {str(e)}"
    #
    # def __modbus_processing(self, CaseData) -> float:
    #     """Modbus数据处理与计算"""
    #     try:
    #         # 从Excel用例获取Modbus参数
    #         modbus_params = {
    #             'ip': CaseData['ip'],
    #             'port': CaseData['port'],
    #             'address': CaseData['address'],
    #             'count': CaseData['count'],
    #             'slave': CaseData['slave'],
    #             'function_code': CaseData['function_code'],
    #             'datatype': CaseData.get('datatype'),
    #             'dataformat': CaseData.get('dataformat')
    #         }
    #         modbus_logger.info(f"Modbus连接参数: {modbus_params}")
    #
    #         # 类型转换关键参数
    #         for param in ['port', 'address', 'count', 'slave', 'function_code']:
    #             modbus_params[param] = int(modbus_params[param])
    #
    #         # 执行Modbus读取
    #         raw_value = self.modb.read_modbus_register(**modbus_params)
    #         if raw_value is None:
    #             raise ValueError("Modbus读取失败")
    #
    #         # 获取计算参数
    #         coefficient = float(CaseData.get('coefficient', 1))
    #         offset = float(CaseData.get('offset', 0))
    #
    #         # 执行计算并保留4位小数
    #         calculated_value = round((raw_value * coefficient) - offset, 4)
    #         modbus_logger.info(f"原始值: {raw_value} → 计算值: {calculated_value}")
    #         return calculated_value
    #
    #     except Exception as e:
    #         modbus_logger.error("Modbus处理异常", exc_info=True)
    #         raise e
    #
    #
    # #初始化写入modbus数据:modbus_client,若不需要写入数据，在test001后括号内删除modbus_client即可。
    # @pytest.mark.parametrize("CaseData", AllCaseData)
    # def test_001(self, CaseData, modbus_client):
    #     record_id = CaseData.get("record_id")
    #     Mongomysqlresult = CaseData.get("Mongomysqlresult")
    #
    #     logging.info(f"开始执行测试用例: {CaseData['Title']}")
    #     # self.dynamic_title(CaseData)
    #     # 写入结果配置
    #     row = CaseData.get("id", None)
    #     # DB_RESULT_COL = 20
    #     # MODBUS_RESULT_COL = 15
    #
    #     try:
    #         # 数据库结果处理
    #         db_result = self.__mysql_mongodb_extraction(CaseData)
    #         FileDataDriver.writeDataToExcel(
    #             row = row,
    #             column = DB_RESULT_COL,
    #             value = str(db_result)[:255] #限制写入字符长度
    #         )
    #
    #         # 写入飞书
    #         feishu_test_case.FeishuTestCase(app_id, app_secret, app_token, table_id).updata_bitable_data(record_id, Mongomysqlresult)
    #
    #
    #
    #         # Modbus数据处理
    #         modbus_result = self.__modbus_processing(CaseData)
    #         FileDataDriver.writeDataToExcel(
    #             row=row,
    #             column=MODBUS_RESULT_COL,
    #             value=modbus_result
    #         )
    #         logging.debug(f"数据库查询结果: {db_result}")
    #         logging.debug(f"Modbus提取结果: {modbus_result}")
    #
    #         # 断言处理逻辑
    #         ASSERT_RESULT_COL = 21   #写入列号
    #         try:
    #             # 类型统一处理
    #             db_num = float(db_result) if isinstance(db_result, (int, float, str)) else None
    #             modbus_num = float(modbus_result)
    #
    #             if db_num is None:
    #                 assert_result = "Skip（无数据库结果）"
    #             elif abs(db_num - modbus_num) <= 0.001:  # 允许千分之一的误差
    #                 assert_result = "Pass"
    #             else:
    #                 assert_result = f"Fail（差值：{abs(db_num - modbus_num):.4f}）"
    #
    #         except (ValueError, TypeError) as e:
    #             assert_result = f"Error（类型错误：{str(e)}）"
    #         except Exception as e:
    #             assert_result = f"Error（未知错误：{str(e)}）"
    #
    #         # 写入断言结果
    #         FileDataDriver.writeDataToExcel(
    #             row=row,
    #             column=ASSERT_RESULT_COL,
    #             value=assert_result
    #         )
    #         # 触发pytest断言
    #         if "Fail" in assert_result:
    #             pytest.fail(assert_result)
    #
    #     except Exception as e:
    #         error_msg = f"测试失败: {str(e)}"
    #         logging.critical("用例执行失败", exc_info=True)
    #         # 同时写入两个结果列
    #         FileDataDriver.writeDataToExcel(
    #             row=row,
    #             column=DB_RESULT_COL,
    #             value=error_msg
    #         )
    #         FileDataDriver.writeDataToExcel(
    #             row=row,
    #             column=MODBUS_RESULT_COL,
    #             value=error_msg
    #         )
    #         pytest.fail(error_msg)