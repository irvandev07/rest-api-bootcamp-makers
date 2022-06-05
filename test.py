from base64 import b64encode
import base64
from flask import Flask, Request, Response, jsonify, request

import requests



app = Flask(__name__)

# @app.route('/hello')
# def welcome():
#     nama = request.args.get('name')
#     return 'hello ' + nama

# @app.route('/hello-json', methods= ['GET', 'POST'])
# def no2():
#     nama = request.args.get('name')
#     data = {'message': 'Hallo '+nama}
#     return data

# @app.route('/weather', methods=['GET'])
# def weather():
#     city = request.headers.get('city')
#     response = requests.get("https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=0af7650b00321f8081a8a9ad3a838f51")
#     data = {
#         'city' : response.json()['name'],
#         'weather' : response.json()['weather'][0]['main'],
#         'coord' : response.json()['coord'],
#         'temp' : response.json()['main']['temp']
#     }
#     return data

# @app.route('/car-manufacturer', methods=['GET','POST'])
# def car_manufaktur():
#     # b = 'dXNlcm5hbWU6cGFzc3dvcmQ='
#     # c = base64.b64decode(b)
#     # e = c.decode("ascii")
#     coba = request.headers.get('Authorization')
#     c = base64.b64decode(coba[6:])
#     e = c.decode("ascii")
#     lis = e.split(':')
#     username = lis[0]
#     passw = lis[1]
#     # return c
#     # header = { 'Authorization' : 'Basic %s' %  userAndPass }
#     # return e
#     if (username == 'admin') & (passw == 'irvan!') :
#         data = request.get_json()
#         response = requests.get("https://vpic.nhtsa.dot.gov/api/vehicles/getallmanufacturers?format=json")
#         x = response.json()['Results']
#         y = []
#         for i in x:
#             if i['Country'] == data['Country']:
#                 y.append(i['Mfr_Name'])
#         return str(y)
#     else:
#         return 'UNAUTHORIZED', 401

# def get_auth(auth):
#     if auth:
#         encode_var = base64.b64decode(auth[6:])
#         string_var = encode_var.decode('ascii')
#         lst = string_var.split(':')
#         username = lst[0]
#         password = lst[1]
#         if ((username == 'admin') & (password == 'irvan!')) or ((username == 'user1') & (password == 'us3r1')) or ((username == 'user2') & (password == 'us3r2')):
#             return True
#     else:
#         return False

# @app.route('/weather-auth', methods=['GET'])
# def data():
#     decode_var = request.headers.get('Authorization')
#     allow = get_auth(decode_var)
#     if allow == True:
#         # return "Success"
#         city = request.headers.get('city')
#         response = requests.get("https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=0af7650b00321f8081a8a9ad3a838f51")
#         data = {
#             'city' : response.json()['name'],
#             'weather' : response.json()['weather'][0]['main'], 
#             'coord' : response.json()['coord'],
#             'temp' : response.json()['main']['temp']
#         }
#         return data
#     else :
#         return "UNAUTHORIZED", 401

# def data(n):
#     shared = 5
#     cumulative = []
#     for x in range(0,int(n)):
#         liked = shared//2
#         shared = liked*3
#         cumulative.append(liked)
#     return {"hasil" : sum(cumulative)}

# @app.route('/viral-advert', methods=['GET'])
# def handler():
#     result = request.args.get('input')
#     return data(result)

# def data(n,m,s):
#     if (m + s - 1) % n == 0:
#         return {'result': n}
#         # return jsonify(n)
#     else:
#         return {'result': ((m + s - 1) % n)}
#         # return jsonify(((m + s - 1) % n))

# @app.route('/save-prisoner', methods=['GET', 'POST'])
# def handler():
#     result = request.get_json()
#     n = result['n']
#     m = result['m']
#     s = result['s']
#     return data(n,m,s)


# @app.route('/save-the-prisoners3/prisoners/<int:prisoners>/candy/<int:candy>', methods=['POST'])
# def handler_path(prisoners,candy):
#     if request.args.get('start') != None:
#         start = int(request.args.get('start'))
#     else:
#         start = 1
#     return (data(prisoners,candy,start))

#--------------------------------------------- TUGAS 1

# def circularArray(a, k, queries):
#     n=len(a)
#     ans=[]
#     for q in queries:
#         ans.append(a[(n-k+q)%n])
#     return {'result' : ans}

# @app.route('/circular-array')
# def handler():
#     req = request.get_json()
#     k = int(request.headers.get('rotation-count'))
#     a = req['data']
#     queries = req['query']
#     return circularArray(a,k,queries)


#-------------------------------------TUGAS 2-3


def findDigits(n):
    # Write your code here
    count = 0
    print(list(str(n)))
    for i in list(str(n)):
        if int(i) != 0 and n % int(i) == 0:
            count += 1
    return count

# @app.route('/find-digits', methods=['POST'])
# def handler():
#     lst = []
#     req = request.get_json()['check']
#     for x in range(len(req)):
#         lst.append(str(findDigits(req[x])))
#     return {'result': lst }

@app.route('/find-digits2', methods=['POST'])
def handler2():
    lst = []
    req = request.get_json()['check']
    for x in range(len(req)):
        output = {
            'input' : req[x],
            'output' : findDigits(req[x])
        }
        lst.append(output)
    return {'result': lst }