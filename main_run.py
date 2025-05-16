#
import pytest
import os
#
#
#
if __name__ == '__main__':
#     # -v 详细信息打印、 -s 标准输出，希望在allure报告当中显示，那么这个位置不要填
#     # "--alluredir", "./result" : 运行之后产生的数据，生成到当前目录下result
#     #  "--clean-alluredir": 每一次运行之前清除历史数据
#
#     #  1. 生成运行之后的数据源
    pytest.main(["-vs", "./testcase/test_run.py"])
#     # , "--alluredir", "./result", "--clean-alluredir"]
#
#     # 2. 把数据源转成html 报告--allure报告
#     # os.system(命令) 在cmd当中输入命令
#     # os.system("allure generate ./result -o ./report_allure --clean")


# import pytest
# import os
# from datetime import datetime
#
# if __name__ == '__main__':
#     # 创建日志目录（如果不存在）
#     log_dir = "./logdata"
#     os.makedirs(log_dir, exist_ok=True)
#
#     # 生成基于时间的日志文件名
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     log_file = f"{log_dir}/log_{timestamp}.log"
#
#     # 运行命令，并动态生成文件名
#     pytest.main([
#         "-vs",
#         "./testcase/test_run.py",
#         f"--log-file={log_file}"
#     ])

    # Allure 报告部分（如果需要）
    # result_dir = "./result"
    # report_dir = "./report_allure"
    # os.system(f"allure generate {result_dir} -o {report_dir} --clean")
