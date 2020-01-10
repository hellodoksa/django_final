from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from base64 import b64encode ## byte 배열을 base64로 변경함 (이미지를 출력해주는 포멧임)
import os 
import pandas as pd 
from .models import Table2 #models.py의 Table2 클래스 불러오기  

cursor = connection.cursor()
@csrf_exempt
def list (request) : 
    
    if request.method == 'GET' :
        request.session['hit'] = 1 #리스트에 진입하면 세션에 hit=1
        sql = """
            SELECT 
                NO, TITLE, WRITER,
                HIT, TO_CHAR(REGDATE, 'YYYY-MM-DD HH:MI:SS')
            FROM
                BOARD_TABLE1
            ORDER BY NO DESC
            """
        
        cursor.execute(sql)
        data = cursor.fetchall()
        
        return render (request, 'board/list.html',{"list":data})
# Create your views here.
@csrf_exempt
def write (request) :
    if request.method == 'GET' : 
        return render (request, 'board/write.html')
    elif request.method =='POST' : 
        
        tmp = None 
        if 'img' in request.FILES :
            img = request.FILES['img']
            tmp = img.read()
        '''
        try : 
            img = request.FILES['img'] ##이미지 들어오는거 
            if img :
                tmp = img.read()
        except :
            pass '''
        arr =[
            request.POST['title'],
            request.POST['content'],
            request.POST['writer'],
            tmp
        ]
        try : 
            sql = """
            INSERT INTO BOARD_TABLE1(TITLE,CONTENT,WRITER,IMG,HIT,REGDATE) 
            VALUES(%s, %s, %s, %s,0, SYSDATE)
            """
            cursor.execute(sql,arr)
        except Exception as e :
            print(e)
        
        return redirect('/board/list')


@csrf_exempt
def content (request) :
    if request.method == "GET":
        no = request.GET.get('no',0)
        if no ==0 :
            return redirect ("board/list")

        if request.session['hit'] == 1 :
        # 조회수 1 증가 시키기 
            sql = """
                UPDATE 
                    BOARD_TABLE1 SET HIT=HIT+1
                WHERE
                    NO = %s

            """
            cursor.execute(sql,[no])
            request.session['hit'] = 0

        #이전 글 번호 가져오기     ##NVL => 값이 null이면 0이 된다. 
        sql = """
                SELECT NVL(MAX(NO),0)  
                FROM   BOARD_TABLE1
                WHERE  NO < %s  
            """
        cursor.execute(sql,[no])
        prev = cursor.fetchone()

        #다음 글 번호 가져오기
        sql = """
                SELECT NVL(MIN(NO),0)
                FROM   BOARD_TABLE1
                WHERE  NO > %s  
            """
        cursor.execute(sql,[no])
        daum = cursor.fetchone()

        #내용 가져오기
        sql = """
            SELECT 
                NO, TITLE, CONTENT, WRITER, 
                HIT, TO_CHAR(REGDATE, 'YYYY-MM-DD HH:MI:SS'),
                IMG
            FROM
                BOARD_TABLE1
            WHERE 
                NO = %s
        """
        cursor.execute(sql,[no])
        data = cursor.fetchone()
        print(data)
        if data[6] :
            img = data[6].read() ### 바이트 배열을 img에 넣음 
            img64 = b64encode(img).decode("utf-8")
        else :
            file = open('./static/img/images.jpg','rb')
            img = file.read()
            img64 = b64encode(img).decode("utf-8")
        return render(request,"board/content.html",{"one":data , 'image':img64, 'prev' :prev[0] , 'next' : daum[0]})
@csrf_exempt
def edit (request) :
    if request.method == 'GET' :
        no = request.GET.get("no",0)
        sql = """
            SELECT 
                NO, TITLE, CONTENT
            FROM 
                BOARD_TABLE1
            WHERE 
                NO = %s
            """
        cursor.execute(sql,[no])
        data = cursor.fetchone()
        return render(request,"board/edit.html",{"one":data })

    elif request.method == 'POST' : 
        no = request.POST['no']
        ti = request.POST['title'] 
        co = request.POST['content']

        arr = [ti, co, no]
        sql = """
            UPDATE BOARD_TABLE1 SET TITLE=%s, CONTENT=%s
            WHERE NO=%s
        """
        cursor.execute(sql,arr)
        return redirect("/board/content?no=" + no) 
@csrf_exempt
def delete(request) :
    if request.method =='GET' :
        no = request.GET.get("no",0)
        sql = """
            DELETE  
                FROM BOARD_TABLE1
            WHERE 
                NO= %s
            """
        cursor.execute(sql,[no])
        return redirect("/board/list")
@csrf_exempt
def dataframe (request) :
    if request.method =='GET' :
        df = pd.read_sql(   ###pandas에서 sql 문 ###
            """
            SELECT NO, TITLE, WRITER,HIT, REGDATE
            FROM BOARD_TABLE1 
            """, con=connection)
    print(df, type(df))
    return render(request, 'board/dataframe.html', {"df" : df.to_html(classes="container" )}) ##원하는 클래스 형식으로보내준다.     

####################################################################################################################################
@csrf_exempt
def t2_insert (request) : 
    if request.method =='GET' :
        return render(request, 'board/t2_insert.html')
    elif request.method == 'POST' : 
        obj = Table2() # 객체 생성
        obj.name = request.POST['name']
        obj.kor = request.POST['kor']
        obj.eng = request.POST['eng']
        obj.math = request.POST['math']
        obj.save()

        return redirect("/board/t2_list" )
        
@csrf_exempt
def t2_list (request) : 
    if request.method =='GET' :
        rows = Table2.object.all()
        #print("@@:",type(rows))
        return render(request, 'board/t2_list.html',{"list" : rows})

@csrf_exempt
def t2_delete (request) : 
    if request.method =='GET' :
        n = request.GET.get("no",0) 
        row = Table2.object.get(no=n)
        row.delete()
        return redirect ("/board/t2_list")

@csrf_exempt
def t2_update (request) : 
    if request.method =='GET' :
        n = request.GET.get("no",0) #누른 메뉴의 no값이 나와야함
        row = Table2.object.get(no=n)  #그 no의 값을 갖고 온다.  
        return render (request,'board/t2_update.html',{"one":row})
    elif request.method == 'POST' : 
        n = request.POST['no']

        #받은 값을 저장하는 방법 
        obj = Table2.object.get(no=n)
        obj.name = request.POST['name']
        obj.kor = request.POST['kor']
        obj.eng = request.POST['eng']
        obj.math = request.POST['math']
        obj.save() ## 꼭 저장까지 하기 
        # UPDATE BOARD_TABLE2 SET
        # NAME=%s, KOR=%s, ENG =%s, MATH=%s
        # WHERE NO=%s

        return redirect("/board/t2_insert" )


## @csrf_exempt # 내가 보낸 데이터인지 확인 시켜준다
def t2_insert_all (request) : 
    if request.method =='GET' :      
        a=range(3)
        print(type(a))
        return render(request,'board/t2_insert_all.html', {"cnt":range(3)})
    elif request.method =='POST' :
        na = request.POST.getlist('name[]')
        ko = request.POST.getlist('kor[]')
        en = request.POST.getlist('eng[]')
        ma = request.POST.getlist('math[]')

        objs = [] 
        # 반복문으로 돌리다가 끊기면 낭패기 때문에 한번에 넣도록 해야한다. 
        for i in range(0,len(na),1) :
            obj = Table2()
            obj.name = na[i]
            obj.kor= ko[i]
            obj.eng = en[i]
            obj.math=ma[i]
            objs.append(obj)


        Table2.object.bulk_create(objs)
        print(objs)
        return redirect("/board/t2_list")


@csrf_exempt       
def t2_update_all (request) : 
    if request.method == 'GET':
        n = request.session['no'] # n = [8, 5 ,3]
        print("get: " ,n)
        # SELECT * FROM BOARD_TABLE2 WHERE NO=8 OR NO=5 OR NO=3
        # SELECT * FROM BOARD_TABLE2 WHERE NO IN (8,5,3)
        rows = Table2.object.filter(no__in=n)  #한번에 리스트 형태로 원하는 값들을 받기 위해
        return render(request, 
            'board/t2_update_all.html', {"list":rows})
    elif request.method == 'POST':
        print("post" )
        menu = request.POST['menu']
        if menu == '1':
            no = request.POST.getlist("chk[]")
            request.session['no'] = no
            print("1",no)
            return redirect("/board/t2_update_all")
        elif menu == '2':
            no = request.POST.getlist("no[]")
            name = request.POST.getlist("name[]")
            kor = request.POST.getlist("kor[]")
            eng = request.POST.getlist("eng[]")
            math = request.POST.getlist("math[]")
            print("2",no)
            objs = []
            for i in range(0, len(no),1):
                obj = Table2.object.get(no=no[i])
                obj.name = name[i]
                obj.kor = kor[i]
                obj.eng = eng[i]
                obj.math = math[i]
                objs.append(obj)
                
            Table2.object.bulk_update(objs,
                    ["name","kor","eng","math"]) ##바꿀 변수명을 지정 해줌 
            return redirect ('/board/t2_list')

    '''if request.method =='GET' :  
        n = request.session['no']
        
            #"SELECT * FROM BOARD_TABLE2 WHERE NO IN (8,5,3)"
            #"SELECT * FROM BOARD_TABLE2 WHERE NO=8 OR NO=5 NO=3 "
        
        rows = Table2.object.filter(no__in=n)
        print(rows)
        return render(request, 'board/t2_update_all.html',{"list":rows})
    elif request.method =='POST' :
        menu = request.POST['menu']
        if menu == str(1) : 
            no = request.POST.getlist("chk[]")
            request.session['no'] =no  ##화면이 바뀌면 값이 없어지기 때문에 세션에다가 값을 받는다. 
            print (no)
            return redirect("/board/t2_update_all")
        elif menu== str(2):
            no = request.POST.getlist("no[]")
            name = request.POST.getlist("name[]")
            kor = request.POST.getlist("kor[]")
            eng = request.POST.getlist("eng[]")
            math = request.POST.getlist("math[]")

            objs = []
            for i in range(0,len(no),1) :
                obj = Table2.object.get(no=no[i])
                obj.name = name[i]
                obj.kor = kor[i]
                obj.eng = eng[i]
                obj.math = math[i]
                objs.append(obj)
            Table2.object.bulk_create(objs)
            print("No 2 ")
            return redirect("/board/t2_list")'''