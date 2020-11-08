from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Shorts


def show(request):
    shorts = Shorts.objects.filter(star__gt=3)

    if 'q' in request.GET:
        # 从已选到的过滤。获取 url 传过来的参数：request.GET['q']，request.GET 是字典。
        shorts = shorts.filter(short__contains=request.GET['q'])

    return render(request, 'index.html', locals())


def index(request):
    return HttpResponse('你好。')
