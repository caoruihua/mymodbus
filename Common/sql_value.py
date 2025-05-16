import allure
import pymysql
from config import *
from pymongo import MongoClient, DESCENDING
from pymongo.errors import PyMongoError
import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class GETSQLVALUE:

    @allure.step(">>>>>>提取mysql数据库的数据")
    @staticmethod #静态方法，直接通过类名调用，不要self
    def get_mysql_value(sql, index=0):
        """
        :param sql:数据查询语句
        :param index: 默认0
        :return: 数据库语句查询结果
        """
        connection = None
        cursor = None
        try:
            connection = pymysql.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                db=DB_DBNAME,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = connection.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()
            return result[index] if result else None
        except Exception as e:
            logger.error(f"MySQL查询错误: {str(e)}")
            return None
        finally:
            if cursor:
                cursor.close()
                print("连接关闭了")
            if connection:
                connection.close()

class ProcessMongodbData:
    @staticmethod
    @allure.step(">>>>>>提取mongodb数据库的数据")
    def get_mongodb_value(query_params=None , collection=None):
        """
        连接MongoDB并提取数据的通用方法
        query_params:并查询条件的字典（包含 'query_condition' 和 'projection' 键）
        collection：mongo文档表名
        """
        # 处理默认值，避免可变对象陷阱
        if query_params is None:
            query_params = {}

        try:
            # 建立连接（含认证处理）
            client = MongoClient(Local_Example_MONGO_HOST)

            # 获取数据库和集合对象
            db = client[Local_Example_MONGO_DBNAME]
            collection = db[collection]

            # 执行查询
            cursor = collection.find_one(sort=[('Getdatetime', DESCENDING)])

        except StopIteration:
            logger.warning("MongoDB查询结果为空")
            return None

        except PyMongoError as e:
            logger.error(f"MongoDB操作失败: {str(e)}")
            return None

        except Exception as e:
            logger.error(f"系统错误: {str(e)}")
            return None


        finally:
            if 'client' in locals():
                client.close()
                logger.info("MongoDB连接已关闭")

        if isinstance(cursor, dict):
            selected_cursor_value = cursor.get(query_params)
            # 判断如果是模块List使用该方法
            if query_params in ["evList","etList"]:
                return selected_cursor_value[0][0]
            elif "List" in query_params:
                return selected_cursor_value[0]
            else:
                return selected_cursor_value

        else:
            return cursor
#
if __name__ == "__main__":
    query_params = "MVMaxList"
    auth = None  # 使用配置文件中的认证信息
    collection = 'RackDetail_TK4070108001-1'

    # 调用函数
    result = ProcessMongodbData().get_mongodb_value(query_params, collection)
    print(result)


