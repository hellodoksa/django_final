from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import pandas as pd 
import matplotlib.pyplot as plt 
import io
import base64
from matplotlib import font_manager, rc 

#djano 에서 제동하는 User 모델 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login1
from django.contrib.auth import logout as auth_logout1
from .models import Table2

from django.db.models import Sum,Min,Max,Count,Avg
cursor = connection.cursor()

def join1 (request) :
    if request.method == 'GET' :
        return render(request, 'member/join1.html')
# Create your views here.
def index(request) :
    #return HttpResponse("index page")
    return render(request, 'member/index.html')

@csrf_exempt
def login(request) :
    if request.method == 'GET':
        return render(request, 'member/login.html')
    elif request.method == 'POST' :
        ar =[request.POST['id'],request.POST['pw']]
        sql = """
        SELECT * FROM MEMBER WHERE ID=%s AND PW=%s
        """
        cursor.execute(sql,ar)
        data = cursor.fetchone()  #한줄만 가져와라 ##아이디는 고유값이기 때문에 값이 하나만 있거나 없거나이다. 
        print(type(data))
        print ("login : " , data)

        if data : 
            request.session['userid'] = data[0]
            request.session['username'] = data[1]
            return redirect('/member/index')

        return redirect('/member/login')

@csrf_exempt
def logout (request) : 
    if request.method =='GET' or request.method =='POST' :
        del request.session['userid']
        del request.session['username']
        return redirect ('/member/index')
@csrf_exempt
def delete (request) : #
    if request.method =='GET' or request.method =='POST' :
        ar = [ request.session['userid'] ]
        sql = "DELETE FROM MEMBER WHERE ID=%s"
        cursor.execute(sql,ar)

        return redirect("/member/logout")
@csrf_exempt
def edit (request) : 
    if request.method == 'GET':
        ar = [ request.session['userid'] ]
        sql = """
            SELECT * FROM MEMBER WHERE ID=%s
        """
        cursor.execute(sql, ar) 
        data = cursor.fetchone()   
        print(data)

        return render(request, 'member/edit.html',{"one":data}) 
    elif request.method =='POST' :
        ar = [
            request.POST['name'],
            request.POST['age'],
            request.POST['id'],
        ]
        
        sql = """
            UPDATE MEMBER SET NAME=%s, AGE=%s
            WHERE ID=%s
        """
        cursor.execute(sql, ar)
        return redirect("/member/index")

@csrf_exempt  ## post로 값을 전달 받는 곳에는 필수적으로 있어야함  ##보안 관련 
def join(request) : 
    if request.method == 'GET': 
        return render(request, 'member/join.html')
    elif request.method == 'POST' :
        id = request.POST['id']
        na = request.POST['name']
        ag = request.POST['age']
        pw = request.POST['pw']

        ar =[id,na,ag,pw]

        print("join :",ar)


        ##SQL LITE로 할때 
        
        sql="""
            INSERT INTO MEMBER(ID,NAME,AGE,PW,JOINDATE) 
            VALUES(%s, %s,%s,%s,SYSDATE)  
            """ ##ar에 있는 값들을 순서대로 넣어라
            ## insert into 테이블명 그리고 넣을 값들 
        cursor.execute(sql,ar)

        
        ##크롬에서 127.0.0.1:8000/member/indx 엔터키를 누른거 같이 
        return redirect('/member/index')  ##앞에 /이 붙어야 한다. 

def list1 (request):
    #id 기준으로 오름차순
    sql = 'SELECT * FROM MEMBER ORDER BY ID ASC'
    cursor.execute(sql)
    data = cursor.fetchall()
    print(type(data))
    print(data)


    #list.html 표시하기 전에 
    #list 변수에 data값을 title 변수에 "회원목록" 문자를
    return render(request , 'member/list.html',
    {"list":data, "title":"회원목록"})
#########################################################################################################
@csrf_exempt 
def auth_join(request) : 
    if request.method == 'GET' :
        return render (request, 'member/auth_join.html')
    elif request.method =='POST' : 
        id = request.POST['username']
        pw = request.POST['password']
        na = request.POST['first_name']
        em = request.POST['email']

        obj = User.objects.create_user(
            username = id, 
            password=pw,
            first_name = na,
            email= em 
        )
        obj.save()

        return redirect ('/member/auth_index')
@csrf_exempt 
def auth_index(request) : 
    if request.method == 'GET' :
        return render (request, 'member/auth_index.html')

@csrf_exempt 
def auth_login(request) : 
    if request.method == 'GET' :
        return render (request, 'member/auth_login.html')
    elif request.method == 'POST' :
        id = request.POST['username']
        pw = request.POST['password']

        #db에 인증 
        obj = authenticate(request, 
        username = id, password=pw)

        if obj is not None:
            auth_login1(request,obj)
            return redirect('/member/auth_index')

        return redirect('/member/auth_login')
@csrf_exempt 
def auth_logout (request) :
    if request.method == 'GET'  or  request.method == 'POST' :
        auth_logout1(request)
        return redirect("/member/auth_index") 
@csrf_exempt 
def auth_edit (request) :
    if request.method == 'GET' :
        if not request.user.is_authenticated :
            return redirect('/member/auth_login')
        obj = User.objects.get(username = request.user)
        return render(request,'member/auth_edit.html' , {"obj":obj})

    elif request.method == "POST" : 
        id = request.POST['username']
        na = request.POST['first_name']
        em = request.POST['email']

        obj = User.objects.get(username =id)
        obj.first_name = na
        obj.email = em
        obj.save()
        return redirect("/member/auth_index")
@csrf_exempt 
def auth_pw (request) :
    if request.method == 'GET' :
        if not request.user.is_authenticated :
            return redirect('/member/auth_login')
        return render(request,'member/auth_pw.html')
    elif request.method == 'POST' :
        pw = request.POST['pw']  # 기존 암호
        pw1 = request.POST['pw1']

        #바꾸기 전에 인증 
        obj = authenticate(request, username = request.user, password = pw)
        if obj :
            obj.set_password(pw1)
            obj.save()
            return redirect ("/member/auth_index")
        return redirect("/member/auth_pw")


        #######################################################


@csrf_exempt 
def exam_insert(request) : 
    if request.method == 'GET' :
        return render (request, 'member/exam_insert.html')
    elif request.method =='POST' : 

        obj = Table2() # 객체 생성

        obj.name = request.POST['name1']
        print("@@ : ",  type(obj.name) , obj.name)
        obj.kor = request.POST['kor']
        obj.eng = request.POST['eng']
        obj.math = request.POST['math']
        obj.classroom = request.POST['class']
        obj.save()

        return redirect ('/member/exam_index')


@csrf_exempt 
def exam_index(request) : 
    if request.method == 'GET' :        
        return render (request, 'member/exam_index.html')

@csrf_exempt 
def exam_update(request) : 
    if request.method == 'GET' :    
        n = request.GET.get("no",0) #누른 메뉴의 no값이 나와야함
        row = Table2.object.get(no=n)  #그 no의 값을 갖고 온다.  
        return render (request, 'member/exam_update.html',{"one":row})
    elif request.method =='POST' :
        n = request.POST['no']

        #받은 값을 저장하는 방법 
        obj = Table2.object.get(no=n)
        obj.name = request.POST['name']
        obj.kor = request.POST['kor']
        obj.eng = request.POST['eng']
        obj.math = request.POST['math']
        obj.classroom = request.POST['classroom']
        obj.save() ## 꼭 저장까지 하기 
        # UPDATE BOARD_TABLE2 SET
        # NAME=%s, KOR=%s, ENG =%s, MATH=%s
        # WHERE NO=%s

        return redirect("/member/exam_insert" )
        
@csrf_exempt
def exam_delete (request) : 
    if request.method =='GET' :
        n = request.GET.get("no",0) 
        row = Table2.object.get(no=n)
        row.delete()
        return redirect ("/member/exam_index")
        
@csrf_exempt
def exam_select(request):
    no = request.GET.get('no',0)

    # SELECT SUM(math) FROM MEMBER_TABLE2 
    list = Table2.object.aggregate(Sum('math'))

    # SELECT NO, NAME FROM MEMBER_TABLE2
    list = Table2.object.all().values('no','name')

    # SELECT * FROM MEMBER_TABLE2 ORDER BY name ASC
    list = Table2.object.all().order_by('name')
    #list = Table2.objects.raw("SELECT * FROM MEMBER_TABLE2 ORDER BY name ASC")

    # 반별 국어, 영어, 수학 합계
    # SELECT SUM(kor), SUM(eng), SUM(math)
    # FROM MEMBER_TABLE2
    # GROUP BY CLASSROOM
    if no == '1':
        list = Table2.object.values('classroom').annotate(kor=Sum('kor'),eng=Sum('eng'),math=Sum('math'))    
    return render(request, 'member/exam_select.html',{"list":list}) 


@csrf_exempt
def dataframe(request):
    #SELECT * FROM MEMBER TABLE2
    #rows= Table2.object.all()

    #1. QuerySet을 List로 변경
    # SELECT NO,NAME,KOR FROM MEMBER_TABLE2
    rows= list(Table2.object.all().values("no","name","kor","eng","math"))  ## html에서 반복문을 돌려야 값이 나온다.
    print(type(rows)) # QuerySet -> list로 변경
    print("QQ : ", rows)

    #2. List를 Dataframe으로 변경
    df=pd.DataFrame(rows)
    print(df)

    #3. dataframe -> list 
    rows1 = df.values.tolist() ## list로 바꾼다. 
    print(rows1)


    return render(request,'member/dataframe.html' , {"df_table" : df.to_html(), "list":rows})   

def graph(request) :
    font_name = font_manager\
        .FontProperties(fname="c:/Windows/Fonts/malgun.ttf") \
        .get_name()
    rc('font',family=font_name)

    ##@SELECT SUM("kor") AS sum1 FROM MEMBER_TABLE2  ##명칭을 바꾼다. 
    #sum_kor = Table2.object.aggregate(Avg("kor"))  ## kor 값의 모든 합을 가져온다. 


    ##@ SELECT SUM("kor" ) FROM MEMBER_TABLE2 WHERE KOR < 10
    ## > gt / >= gte/  < lt / <= lte
    ##sum_kor  = Table2.object.filter(classroom = "3").aggregate(kor__avg = Avg("kor")) ## 3반의 국어 성적을 더해보자
    ##sum_eng  = Table2.object.aggregate(Avg("eng"))
    ##sum_math = Table2.object.aggregate(Avg("math"))

    '''##@SELECT "MEMBER_TABLE2".CLASSROOM",
    #           SUM("MEMBER_TABLE2",'KOR') AS sum_kor , 
    #           SUM("MEMBER_TABLE2",'ENG') AS sum_eng, 
    #           SUM("MEMBER_TABLE2",'MATH') AS sum_math 
    # FROM MEMBER_TABLE2 
    # GROUP BY 
    #           "MEMBER_TABLE2"."CLASSROOM" 
    sum_ = Table2.object.values("classroom").annotate(kor_avg=Avg("kor"),eng_avg=Avg("eng"),math_avg=Avg("math"))
    print(sum_.query)
    df = pd.DataFrame(sum_)
    print(df)
    df = df.set_index('classroom')
    print(df)
    print(df.columns)
    df.plot(kind="bar")'''


    #모든 합 출력 
    all_sum = [] # [[1반의 국영수 평균], [2반의 국영수 평균], ... ]
    
    for i in range(1,4) :
        i = str(i)
        sum_kor  = Table2.object.filter(classroom = i).aggregate(kor__avg = Avg("kor")) # => sum_kor = {"kor_avg" : 16}
        sum_eng  = Table2.object.filter(classroom = i).aggregate(eng__avg = Avg("eng"))
        sum_math  = Table2.object.filter(classroom = i).aggregate(math__avg = Avg("math"))
        x = ['kor','eng','math']
        y = [sum_kor["kor__avg"],sum_eng['eng__avg'],sum_math['math__avg']]
        
        plt.bar(x,y)
        plt.title(i +"반의 국영수 평균 성적")
        plt.xlabel("과목별")
        plt.ylabel("과목성적 평균")

        #plt.show()# 표시 하라
        plt.draw() #안보이게 그림을 캡쳐 

        img = io.BytesIO() # img에 byte배열로 보관
        plt.savefig(img, format="png")
        img_url = base64.b64encode(img.getvalue()).decode()

        all_sum.append(img_url)
        plt.close()


    new_list=[]
    for i in all_sum : 
        new_list.append("data:;base64,{}".format(i))



    
    return render(request, 'member/graph.html',{"graph1" : new_list})#'data:;base64,{}'.format(all_sum)})

 