import os

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from mysiteapp.models import UserList, AttendanceSheet, FaceData
# Create your views here.
from mysite.settings import MEDIA_ROOT
from mysiteapp.utils import base64_convert_png, face_compare


def index(request):

    return render(request, 'facerecognition/index.html', locals())


def upload_attendance_img(request):
    """
    门禁识别视图
    :param request:
    :return:
    """
    if request.method == 'POST':
        print(1)
        img_base64 = str(request.POST.get('img_data')).split(',')[1]
        temp_img_path = os.path.join(MEDIA_ROOT, 'test.png').replace('/', '\\')
        base64_convert_png(img_base64, temp_img_path)  # base64 转 png
        try:
            user_id_list = face_compare(temp_img_path, FaceData.get_all_photo_encodings())
        except Exception as e:
            return JsonResponse({"flag": 0, "msg": "未检测到人脸信息， 请重新上传！"})
        if len(user_id_list) == 0:
            # os.remove(temp_img_path)
            return JsonResponse({"flag": 0, "msg": "未匹配到您的人脸信息， 请重新上传！"})
        msg = ""
        for user_id in user_id_list:
            att_user = AttendanceSheet(user_id=user_id, attendance_statu=False)
            print(att_user)
            att_user.attendance_statu = True
            att_user.attendance_img.save(name='{}.png'.format(int(timezone.now().timestamp())),
                                         content=open(temp_img_path, 'rb'))
            att_user.save()
            msg += "{}, ".format(att_user.user.user_name)

        if msg != "":
            msg = "欢迎您！"+msg+ "祝您生活愉快，请通行！"
        os.remove(temp_img_path)
        # print(msg)
        return JsonResponse({"flag": 1, "msg":msg})


def attendance_statistics(request):
    """
    门禁识别记录
    :param request:
    :return:
    """
    att_user = AttendanceSheet.objects.all()

    #all_user = UserList.objects.all()
    return render(request, 'facerecognition/attendance_book.html', locals())
