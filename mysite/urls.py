from django.contrib import admin
from django.conf.urls.static import static
from mysiteapp.views import index,upload_attendance_img
from django.urls import path, include

from mysite import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  index, name='index'),  # 首页的url 不能用include
    path('face/', include('mysiteapp.urls', namespace='face')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
