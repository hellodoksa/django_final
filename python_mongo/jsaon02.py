import json
#pip install cx_Oracle 모듈 설치 
import cx_Oracle as oci
import requests 
conn = oci.connect('admin/1234@192.168.99.100:32764/xe',encoding="utf-8")
#커서 생성 
cursor  = conn.cursor()

url = "http://ihongss.com/json/exam4.json"
str1 = requests.get(url).text 
data1 = json.loads(str1)
make_dick = []
num=0
for i in data1 : 
    num += 1 
    name = "people" + str(num)
    print ("name : ", i['name'])
    print ("species : ", i['species'])
    print ("foods - like : ",i['foods']['likes'][0])
    print ("foods - dislike : ",i['foods']['dislikes'][0])
    tmp_dick = {name : {"name" : i['name'], "species": i['species'], "foods - like" :i['foods']['likes'][0] , 
    "foods - dislike" :i['foods']['dislikes'][0] }}
    make_dick.append(tmp_dick)
    print("---------------------------------------------")
print(make_dick)




'''
## exam3 
ret = data1['ret']
ret1 = data1['ret1']
for i in ret1 : 
    sql = """
        INSERT INTO MEMBER(ID,PW,NAME,AGE,JOINDATE) 
        VALUES(:id,'aaa1', :name, :age, SYSDATE)
        """
    cursor.execute(sql,i)
    #cursor.execute(sql,ret1)
conn.commit()
'''
