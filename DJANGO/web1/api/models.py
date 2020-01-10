from django.db import models

# Create your models here.
class Item(models.Model) :
    object = models.Manager() #vs code 오류 제거용 

    no      = models.AutoField(primary_key = True) #기본 키 글번호가 기본 키가 된다. 
    name   = models.CharField(max_length= 30)
    price = models.IntegerField()
    regdate = models.DateTimeField(auto_now_add=True) #날짜타임 자동으로 넣어라 