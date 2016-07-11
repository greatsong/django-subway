#-*- coding: utf-8 -*-
import django
from django.shortcuts import render
from django.http import HttpResponse

import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def compare_form(request):
    return render(request, 'subway201605/main.html',{})

def compare(request):
    data = csv.reader(open('/home/greatsong21/subwayproject/201605subway.csv', 'r'), delimiter=",")
    station1,number1,station2,number2 = request.GET['station1'], request.GET['type1'], request.GET['station2'], request.GET['type2']
    # message = '비교대상: %s(%s) vs %s(%s)' % (request.GET['station1'],request.GET['type1'],request.GET['station2'],request.GET['type2'])
    cnt1 = []
    cnt2 = []
    in1 = []
    in2 = []
    out1 = []
    out2 = []

    for row in data:
        if (row[1] == station1 and row[0] == number1):
            cnt1 = row[2:]
        if (row[1] == station2 and row[0] == number2):
            cnt2 = row[2:]

    in1 = cnt1[::2]
    out1 = cnt1[1::2]
    in2 = cnt2[::2]
    out2 = cnt2[1::2]

    plt.rc('font', family='Malgun Gothic')

    labels = []
    x = []

    for i in range(4, 28):
        labels.append(str(i) + '시')

    x = np.array(range(4,28))
    y = np.array(range(0,24))


    fig = plt.Figure() #figsize=(20, 8)
    fig.add_axes(ax)
    ax = fig.add_subplot(111)
    #ax.set_xticks(x)
    #ax.set_xticklabels(labels, rotation='vertical')
    ax.plot(np.array(10), np.array(10))
    #ax.plot(x, in1, 'r', label=station1 + '역 in')
    #ax.plot(x, in2, 'b', label=station2 + '역 in')
    #ax.plot(x, out1, 'r--', label=station1 + '역 out')
    #ax.plot(x, out2, 'b--', label=station2 + '역 out')
    #ax.set_ylim(ymax=420000)
    #ax.set_title(station1 + '역 승out cnt vs ' + station2 + '역 승out cnt   # 2016년 5월 티머니카드 제공 데이터')
    #ax.legend()

    canvas = FigureCanvas(fig)
    response = django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response


def simple(request):
    data = csv.reader(open('201605subway.csv', 'r'), delimiter=",")

    max_person1 = [0] * 24
    max_station1 = [''] * 24

    max_person2 = [0] * 24
    max_station2 = [''] * 24
    for row in data:
        for i in range(24):
            if int(max_person1[i]) < int(row[2 + (i * 2)]):
                max_person1[i] = row[2 + (i * 2)]
                max_station1[i] = row[1] + '/' + str(i + 4)  # +'('+ row[0]+')'
            if int(max_person2[i]) < int(row[3 + (i * 2)]):
                max_person2[i] = row[3 + (i * 2)]
                max_station2[i] = row[1] + '/' + str(i + 4)  # +'('+ row[0]+')'

    fig = plt.figure(figsize=(20, 8))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    plt.rc('font', family='Malgun Gothic')
    cnt = np.arange(24)
    ax1.set_title('2016년 5월 서울시 지하철 시간대별 최다 in역')
    ax1.plot(cnt, max_person1, 'r')
    ax1.set_xticks(cnt)
    ax1.set_xticklabels(max_station1, rotation = 45, fontsize = 9)
    ax1.set_ylim(ymax=450000)
    ax2.set_title('2016년 5월 서울시 지하철 시간대별 최다 out역')
    ax2.plot(cnt, max_person2, 'b')
    ax2.set_xticks(cnt)
    ax2.set_xticklabels(max_station2, rotation = 45, fontsize = 9)
    ax2.set_ylim(ymax=450000)

    canvas=FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response