from django.shortcuts import render
from django.http import HttpResponse
from .models import Item

#Select1
from .serializers import ItemSerializers
from rest_framework.renderers import JSONRenderer
import json 

def select1(request) :
    key = request.GET.get("key", "")
    num = int(request.GET.get("num", "1"))
    txt = request.GET.get("txt", "")
    data = json.dumps({"ret":'key error'})  

    if key =='abc' :    
        #print(txt)
        obj = Item.object.filter(price__contains=txt)[0:num]
        print(obj)

        serializer = ItemSerializers(obj, many=True)
        data = JSONRenderer().render(serializer.data)

        
 


    return HttpResponse(data)

        

def select2(request) :
    #obj = Item.object.get(no=1)
    obj = Item.object.all()
    serializer = ItemSerializers(obj, many=True)
    data = JSONRenderer().render(serializer.data)
    return HttpResponse(data)

def insert1(request) :
    for i in range(1,31,1) :
        obj =Item()
        obj.name = '물품명' + str(i)
        obj.price = 1123 * i
        obj.save()
    
    return HttpResponse('insert1')