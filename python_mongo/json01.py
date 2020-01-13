import json
#pip install cx_Oracle 모듈 설치 
import cx_Oracle as oci

##이건 장고가 아니여서 오토 커밋이 아니다. COMMIT ! 
#접속하기 
conn = oci.connect('admin/1234@192.168.99.100:32764/xe',encoding="utf-8")
#커서 생성 
cursor  = conn.cursor()
file1= open('./resources/exam2.json')

data = json.load(file1) ##str to dict로 변경
sql = """
        INSERT INTO MEMBER(ID,PW,NAME,AGE,JOINDATE) 
        VALUES(:ID, :PW, :NAME, :AGE, SYSDATE)
    """ ##딕셔너리 키값을 넣자 

cursor.execute(sql,data)
conn.commit()
print(data)
print(type(data))