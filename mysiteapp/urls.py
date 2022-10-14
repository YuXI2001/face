from django.urls import re_path
from . import views

app_name = 'mysiteapp'

urlpatterns = [
    re_path('upload/', views.upload_attendance_img, name='upload'),
    re_path('attendance_all/',views.attendance_statistics,name='statistics')
]
