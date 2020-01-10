## 크롬에서 특정 url에 따라서 어떻게 구동 시키라는지  
from django.urls import path
from . import views 

urlpatterns = [
    path('index', views.index, name='index'), ##주소창에다가 http://127.0.0.1:8000/member/index 일때  => index 함수 동작
    path('join' , views.join , name='join'),  ##http://127.0.0.1:8000/member/join
    path('login', views.login, name='login'),  ##http://127.0.0.1:8000/member/login
    path('list1', views.list1, name='list1'),
    path('join1', views.join1, name='join1'),
    path('logout', views.logout, name='logout'),
    path('edit', views.edit, name='edit'),
    path('delete', views.delete, name='delete'),

    path('auth_join', views.auth_join, name='auth_join'),
    path('auth_index', views.auth_index, name='auth_index'),
    path('auth_login', views.auth_login, name='auth_login'),
    path('auth_logout', views.auth_logout, name='auth_logout'),
    path('auth_edit', views.auth_edit, name='auth_edit'),
    path('auth_pw', views.auth_pw, name='auth_pw'),

    path('exam_index', views.exam_index, name='exam_index'),
    path('exam_insert', views.exam_insert, name='exam_insert'),
    path('exam_update', views.exam_update, name='exam_update'),
    path('exam_delete', views.exam_delete, name='exam_delete'),
    path('exam_select', views.exam_select, name='exam_select'),

    path('dataframe', views.dataframe, name='dataframe'),
    path('graph', views.graph, name='graph'),
]