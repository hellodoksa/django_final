from rest_framework import serializers
from .models import Item
# V과 M 사이에서 object를 직렬화 시켜준다. 
# DB에서 모델을 그대로 저장한다.  

class ItemSerializers(serializers.ModelSerializer) :
    class Meta :
        model = Item
        fields = ('no','name','price','regdate')