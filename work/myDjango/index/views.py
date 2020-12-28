from django.shortcuts import render
from django.http import HttpResponse
from .models import Table1
import re
from collections import defaultdict
from django.db.models import Count
import json
import datetime
# Create your views here.

# 取出全部数据
shorts = Table1.objects.all()


# 构造正则，将太长的标题给剪断
def split(name):
    p = r'.*(?= [45]?[G ]?智能)'
    pattern = re.compile(p)
    cut = pattern.search(name)
    if cut:
        return cut.group()
    return name


# 返回可供 Js 使用的字典类型
def get_rates():
    rates = defaultdict(list)

    for phone_name, in shorts.values_list('phone_name').distinct():  # 解包
        phone = shorts.filter(phone_name=phone_name)
        good = phone.filter(sentiment__gt=0.75).count()
        normal = phone.filter(sentiment__range=[0.5, 0.75]).count()
        bad = phone.filter(sentiment__lt=0.5).count()
        phone_name = split(phone_name)

        rates['phone_name'].append(phone_name)
        rates['good'].append(good)
        rates['normal'].append(normal)
        rates['bad'].append(bad)
    return rates


# 返回 List[dict]
def get_counts():
    amount = shorts.values('phone_name').annotate(s=Count('phone_name'))
    counts = []

    for count in amount:
        phone_name = count['phone_name']
        phone_count = count['s']
        phone_name = split(phone_name)

        # 构建符合特定 javasript 格式的 json 数据
        counts.append({
            'name': phone_name,
            'y': phone_count
        })
        counts[0]['sliced'] = True
        counts[0]['selected'] = True

    return counts


def index(request):
    return HttpResponse('hello, django!')


def show2(request):
    shorts = Table1.objects.all()
    if 'q' in request.GET:
        shorts = shorts.filter(short__contains=request.GET['q'])
    return render(request, 'index2.html', locals())


def bar(request):
    rates = get_rates()
    # 传递到 js 使用，参数必须要 json 化
    return render(request, 'barchart.html',
                  {"rates": json.dumps(rates)})


def pie(request):
    counts = get_counts()
    return render(request, 'piechart.html', {"counts": json.dumps(counts)})


def tables(request):
    return render(request, 'tables.html', {'shorts': shorts})


def charts(request):
    rates = get_rates()
    counts = get_counts()
    return render(request, 'charts.html', {"counts": json.dumps(counts), "rates": json.dumps(rates)})


def show(request):
    rates = get_rates()
    counts = get_counts()
    return render(request, 'index.html',
                  {"counts": json.dumps(counts), "rates": json.dumps(rates), 'shorts': shorts})
