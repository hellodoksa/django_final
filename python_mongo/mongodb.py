import pymongo 
import requests 
import json

conn = pymongo.MongoClient('192.168.99.100',32766)
db = conn.get_database("db1") ## 없으면 생성 있으면 가져오기 
table = db.get_collection("exam20") ##collection 생성 


url = "http://ihongss.com/json/exam21.json"
str1=requests.get(url).text 
data1 = json.loads(str1)
showRange = data1['boxOfficeResult']['showRange']

for i in data1['boxOfficeResult']['dailyBoxOfficeList']:
    dict1 = dict()
    dict1['showRange'] = showRange
    dict1['rankOldAndNew'] = i['rankOldAndNew']
    dict1['movieNm'] = i['movieNm']
    dict1['salesShare'] = i['salesShare']
    dict1['salesAcc'] = i['salesAcc']
    dict1['scrnCnt'] = i['scrnCnt']
    dict1['showCnt'] = ['showCnt']
    table.insert_one(dict1)








'''##exam 10 
for tmp in data1['data'] : 
    print(tmp['id'])
    print(tmp['name'])
    print(tmp['age'])
    print(tmp['score']['math'])
    print(tmp['score']['kor'])
    dict1 = dict()
    dict1['id'] = tmp['id']
    dict1['name'] = tmp['name']
    dict1['age'] = tmp['age']
    dict1['math'] = tmp['score']['math']
    dict1['kor'] = tmp['score']['kor']

    table.insert_one(dict1)'''
    



'''data1 = table.find()
for i in data1 : 
    print(i)
    print(type(i))'''

conn.close()
