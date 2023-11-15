from http import HTTPStatus
import json
from flask import Flask, request, Response
from flasgger import Swagger
import geocode as gc

app = Flask(__name__)
swagger = Swagger(app)

"""
curl -X POST -H "Content-Type: application/json" 
-d '{"address":"广东省电白县霞洞镇","api":"key"}' 
http://localhost:5001/geocoding
"""
@app.route('/geocoding', methods=["GET",'POST'])
def geocoding():
    """
    发送地址（省-市-县/区-街道）和apikey
    ---
    tags:
      - 发送地址，接收返回的地理信息数据，包括经纬度和精确度
    description:
        以json格式返回经纬度信息接口
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: 传入参数信息
          required:
            - address
            - api
          properties:
            address:
              type: string
              description: 中文地址
            api:
              type: string
              description: api密钥（天地图官网免费注册）

    responses:
      200:
          description: 获取成功
          example: {"msg":"ok","location":{"score":81,"level":"兴趣点","lon":111.035428341845,"lat":21.7400617267674,"keyWord":"广东省电白县霞洞镇化普小学"},"searchVersion":"6.4.6V","status":"0"}
    """
    if request.method == "POST":
        address = request.json['address']
        api = request.json['api']
        response = gc.map_world_api(address, api)
        return Response(response, content_type='application/json; charset=utf-8')
    
    if request.method == "GET":
        address = request.args.get('address')
        api = request.args.get('api')
        response = gc.map_world_api(address, api)
        return Response(response, content_type='application/json; charset=utf-8')

"""
curl -X POST -H "Content-Type: application/json" 
-d '{"address":"广东省电白县霞洞镇"}'
http://localhost:5001/dir-geocoding+-
"""
@app.route('/dir-geocoding', methods=['GET','POST'])
def dir_geocoding():
    """
    发送地址（省-市-县/区-街道）和apikey
    ---
    tags:
      - 发送地址，接收返回的地理信息数据，包括经纬度和精确度
    description:
        以json格式返回经纬度信息接口
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: 传入参数信息
          required:
            - address
          properties:
            address:
              type: string
              description: 中文地址

    responses:
      200:
          description: 获取成功
          example: {"msg":"ok","location":{"score":81,"level":"兴趣点","lon":111.035428341845,"lat":21.7400617267674,"keyWord":"广东省电白县霞洞镇化普小学"},"searchVersion":"6.4.6V","status":"0"}
    """
    if request.method == "GET":
        address = request.args.get('address')
        response = gc.map_world_api_no_key(address)
        return Response(response, content_type='application/json; charset=utf-8')

    if request.method == "POST":
        address = request.json['address']
        response = gc.map_world_api_no_key(address)
        return Response(response, content_type='application/json; charset=utf-8')

# @app.route('/', methods=['GET'])
# def hello():
#     return "hello world!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)