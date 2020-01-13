#파일명 : flask01.py
from flask import Flask, render_template, request , redirect
import cx_Oracle as ocl #conda install cx_oracle


conn = ocl.connect('admin/1234@192.168.99.100:32764/xe')
cursor = conn.cursor()

app = Flask(__name__)

@app.route("/")   #뒤에 주소를 친다. 
def index () :
    sql = "SELECT * FROM MEMBER"
    cursor.execute(sql)
    data = cursor.fetchall()
    '''print("@@ : ", type(data))
    print(data)
    all_sum=0
    for i in data : 
        print(i, "|| age : ", i[3])
        all_sum += i[3]

    print("sum = ", all_sum)'''
    return "index page"

## 똑같은 주소가 두개여도 메쏘드가 다르면 가능하다. 
##크롬에서 주소를 처음치면 get 메쏘드로 간다.
@app.route("/join", methods=['GET'])   
def join () :
    #
    return render_template('list.html',list=data)

@app.route("/login", methods=['GET'])   
def login () :
    return render_template('login.html')


#post에서는 화면을 렌더링 해서는 안된다. 
@app.route("/join", methods=['POST'])
def join_post () :
    a = request.form['id']
    b = request.form['pw']
    c = request.form['name']
    d = request.form['age']
    sql = "INSERT INTO MEMBER VALUES(:id, :pw, :na, :ag, SYSDATE)"

    cursor.execute(sql, id=a, pw=b,na=c, ag=d)
    conn.commit()

    #오라클 DB 접속 
    #데이터를 추가하는 SQL문 작성
    #SQL문 수행

    #DB에 값을 넣고 
    #print("{} : {} : {} : {}".format(a,b,c,d))
    #print("join - post")
    return redirect('/') #크롬에서 입력한 것 처럼 동작하자 
    #마치 127.0.0.1/ 처럼 인덱스 페이지
    # 아이피 주소 말고 그 뒤에 친 주소처럼 이동하자   


if __name__ == '__main__' : 
    app.run(debug=True) # 개발 모드이다.
