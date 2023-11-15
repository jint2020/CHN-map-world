import requests
from configparser import ConfigParser
import json


# key =""
# url="""http://api.tianditu.gov.cn/geocoder?ds={"keyWord":"广东省佛山市高明区"}&tk=key"""

# 国家地理信息天地图api
def map_world_api(address = None,key=None):
    if address is None or key is None:
        result = {"status": 400, "msg": "address or key is None"}
        return result
    
    base_url = "http://api.tianditu.gov.cn/geocoder"
    params = {'ds': '{"keyWord": "' + address + '"}',
              'tk': key}
    # 发起GET请求
    response = requests.get(base_url, params=params)

    # 检查HTTP响应状态
    if response.status_code == 200:
        # 解析JSON响应
        
        return response.text
    else:
        # 打印错误信息
        print("Error in Map World API request. Status:", response.status_code)
        return None
    
def map_world_api_no_key(address = None):
    cp = ConfigParser() # create a configparser object
    cp.read("config.ini")
    # read account and password
    key = cp['ACCESS']['key']
    if address is None:
        result = {"status": 400, "msg": "address is None"}
        return result
    
    base_url = "http://api.tianditu.gov.cn/geocoder"
    params = {'ds': '{"keyWord": "' + address + '"}',
              'tk': key}
    # 发起GET请求
    response = requests.get(base_url, params=params)

    # 检查HTTP响应状态
    if response.status_code == 200:
        # 解析JSON响应
        # result_dict = json.loads(response.text)
        # for k,v in result_dict.items():
        #     if isinstance(v, str):
        #         try:
        #             # 尝试解码为UTF-8，如果成功则更新字典中的值
        #             decoded_value = v.encode('latin-1').decode('unicode-escape')
        #             result_dict[k] = decoded_value
        #         except UnicodeDecodeError:
        #             # 如果解码失败，保留原始值
        #             pass
        result_dict = json.loads(response.text)
        if result_dict["location"]["score"] < 80:
            result_dict["location"]["reliable"] = "low reliable"
            return str(result_dict)
        print(type(response.text))
        return response.text
    else:
        # 打印错误信息
        print("Error in Map World API request. Status:", response.status_code)
        return None
