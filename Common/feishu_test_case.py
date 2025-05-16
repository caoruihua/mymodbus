import requests
import json
import schedule


class FeishuTestCase:
    def __init__(self, app_id, app_secret, app_token, table_id):
        self.app_id = app_id
        self.app_secret = app_secret
        self.app_token = app_token
        self.table_id = table_id

    # 获取 tenant_access_token
    def get_tenant_access_token(self):
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = json.dumps({
            "app_id": self.app_id,
            "app_secret": self.app_secret
        })
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # 检查请求是否成功
        return response.json()['tenant_access_token']

    # 获取多维表格数据
    def get_bitable_data(self):
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records/search"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_tenant_access_token()}'
        }
        response = requests.post(url, json={}, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        # 创建列表接收数据
        data = []
        # 把每行数据保存成字段
        # print(response.json()["data"]["items"])
        for fields in response.json()["data"]["items"]:
            record_id = fields["record_id"]
            fieleds_dict = {"record_id": record_id}
            for key, value in fields["fields"].items():
                # 处理返回的数据
                if isinstance(value, list) and value and isinstance(value[0], dict) and 'text' in value[0]:
                    fieleds_dict[key] = value[0]['text']
                elif isinstance(value, dict) and 'value' in value and value['value'] and isinstance(value['value'][0],dict) and 'text' in value['value'][0]:
                    fieleds_dict[key] = value['value'][0]['text']
                else:
                    fieleds_dict[key] = value
            data.append(fieleds_dict)
        return data

    # 更新多维表格数据
    def updata_bitable_data(self, record_id, *args):
        self.record_id = record_id
        self.args = args
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records/{self.record_id}"
        headers = {'Content-Type': 'application/json','Authorization': f'Bearer {self.get_tenant_access_token()}'}
        json = {"fields": {f"{args[0]}": self.args[1]}}
        response = requests.put(url, json=json, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

if __name__ == '__main__':
    from TaokeEms.config import *
    # FeishuTestCase(app_id, app_secret, app_token, table_id, ).updata_bitable_data("recYi7EnJ4", "成功")
    feishu_test_case = FeishuTestCase(app_id, app_secret, app_token, table_id)
    feishu_case_data = feishu_test_case.get_bitable_data()
    for data in feishu_case_data:
        feishu_test_case.updata_bitable_data(data["record_id"], "Mongomysqlresult", "888")
        print("写入成功")
    #
    # feishu_test_case.updata_bitable_data(feishu_case_data)
    # print(feishu_case_data)
