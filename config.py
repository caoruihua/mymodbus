#  用来存放常用的变量，常量一般都是大写
# 应用程序配置


APP_PATH = r"D:\TaokeEms\TaokeEmsClient.exe"# 应用安装路径
BACKEND = "uia" # 默认UI自动化协议
TIMEOUT = 10 # 超时时间(秒)
WINDOW_TITLE = None # 目标窗口标题
CASEDATAURL = "../data/testcaseV0.1.xlsx"

SHEETNAME = 'Sheet1'
#
#   msg
# MSG_OK = "断言成功"
# MSG_NO = "断言失败"
# MSG_DATA_ERROR = "数据解析错误"
# MSG_RESPONSE_ERROR = "响应数据获取失败"

# MSG_MySQL_ERROR = "数据库断言失败"
#
# 测试环境数据库（MySQL）的连接信息
DB_HOST = 'rm-uf674co8dy5525n60ho.mysql.rds.aliyuncs.com'  # 数据库地址
DB_PORT = 3306
DB_USER = 'test_001'  # 数据库用户名
DB_PASSWORD = 'Taoke2021'  # 数据库密码
DB_DBNAME = 'emsdata2025'  # 数据库库名
DB_TABLE= 'sys_detail'    #表名


#云端数据库（MongoDB）连接信息
MONGO_HOST = '127.0.0.1'# 数据库地址
MONGO_PORT = 27017
MONGO_USER = None #数据库用户名
MONGO_PASSWORD = None    #数据库密码
MONGO_DBNAME = "emsData_analyze"   #数据库库名
# MONGO_COLLECTION = 'SysDetail_TS4320240814_20250125'

# 集群数据库
Local_Example_MONGO_HOST = "mongodb://localhost:27017/"
Local_Example_MONGO_DBNAME = "emsData_analyze"

#集群数据库
# JQ_MONGO_URL ="mongodb://RS-01:27017,RS-02:27017/"

# 飞书相关信息
# 应用相关信息, 从飞书开发者后台获取
app_id = "cli_a75bec7099b5d00c"
app_secret = "7pjGJdjbiVNeDCcEH87huhqjloDyjknm"
# 表信息,在飞书中复制连接获取
app_token = "YLnMbpF04adU1es17Psc9fGgn4g"
table_id = "tblK5e7kvbMprrws"