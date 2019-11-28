from django.urls import path
from . import views

app_name = 'front'

urlpatterns= [
    
  path('',views.student_list),
  path('<int:pk>/', views.student_detail),
  path('enter/', views.student_enter),
  path('exit/',views.student_exit),
  path('manual/enter/', views.manual_enter),
  path('manual/exit/', views.manual_exit),
       
]