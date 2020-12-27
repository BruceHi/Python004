from django.shortcuts import render
from django.http import HttpResponse
from .models import Table1
import re
from collections import defaultdict
from django.db.models import Count
import json
import datetime
# Create your views here.


def index(request):
    return HttpResponse('hello, django!')


def show(request):
    shorts = Table1.objects.all()

    if 'q' in request.GET:
        shorts = shorts.filter(short__contains=request.GET['q'])

    return render(request, 'index.html', locals())


def bar(request):
    shorts = Table1.objects.all()
    storage_time = shorts[0].storage_time

    rates = defaultdict(list)

    # 构造正则，将太长的标题给剪断
    p = r'.*(?= [45]?[G ]?智能)'
    pattern = re.compile(p)

    for phone_name, in shorts.values_list('phone_name').distinct():  # 解包
        phone = shorts.filter(phone_name=phone_name)
        good = phone.filter(sentiment__gt=0.75).count()
        normal = phone.filter(sentiment__range=[0.5, 0.75]).count()
        bad = phone.filter(sentiment__lt=0.5).count()

        # 含有：4G智能，5G智能，智能等字段前面是手机名字
        cut = pattern.search(phone_name)
        if cut:
            phone_name = cut.group()

        rates['phone_name'].append(phone_name)
        rates['good'].append(good)
        rates['normal'].append(normal)
        rates['bad'].append(bad)

    # 传递到 js 使用，参数必须要 json 化
    return render(request, 'barchart.html',
                  {"rates": json.dumps(rates), 'storage_time': storage_time})


def pie(request):
    shorts = Table1.objects.all()
    counts = shorts.values('phone_name').annotate(s=Count('phone_name'))

    res = []

    p = r'.*(?= [45]?[G ]?智能)'
    pattern = re.compile(p)

    for count in counts:
        phone_name = count['phone_name']
        phone_count = count['s']

        cut = pattern.search(phone_name)
        if cut:
            phone_name = cut.group()

        # 构建符合特定 javasript 格式的 json 数据
        res.append({
            'name': phone_name,
            'y': phone_count
        })
        res[0]['sliced'] = True
        res[0]['selected'] = True

    return render(request, 'piechart.html', {"res": json.dumps(res)})
