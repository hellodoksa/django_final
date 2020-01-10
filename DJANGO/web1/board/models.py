from django.db import models


#모델을 추가하면 데이터 베이스에 자동으로 추가가 된다. 

class Table1(models.Model) :
    object = models.Manager() #vs code 오류 제거용 

    no      = models.AutoField(primary_key = True) #기본 키 글번호가 기본 키가 된다. 
    title   = models.CharField(max_length= 200)
    content = models.TextField()
    writer  = models.CharField(max_length=50)
    hit     = models.IntegerField()                   # 조회수 
    img     = models.BinaryField(null=True)
    regdate = models.DateTimeField(auto_now_add=True) #날짜타임 자동으로 넣어라 
class Table2(models.Model) : 
    object = models.Manager()

    no      = models.AutoField(primary_key=True) 
    name    = models.CharField(max_length=30)
    kor     = models.IntegerField()
    eng     = models.IntegerField()
    math    = models.IntegerField()
    regdate = models.DateTimeField(auto_now_add=True)

