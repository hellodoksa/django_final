#pip install cx_Oracle 모듈 설치 
import cx_Oracle as oci

##이건 장고가 아니여서 오토 커밋이 아니다. COMMIT ! 
#접속하기 
conn = oci.connect('admin/1234@192.168.99.100:32764/xe',encoding="utf-8")
print(conn)
#커서 생성 
cursor  = conn.cursor()
#SELECT 
sql = "SELECT *FROM MEMBER"
cursor.execute(sql)
data = cursor.fetchall()
print(data)

sql = """
        INSERT INTO MEMBER(ID,PW,NAME,AGE,JOINDATE) 
        VALUES(:1, :2, :3, :4, SYSDATE)
    """
arr = ['aa1', 'aa1' , '길홍동',33]
cursor.execute(sql,arr)
conn.commit()