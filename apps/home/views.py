# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.tiket import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


@login_required(login_url="/login/")
def index(request):
    # tiket = models.MoveState.objects.all()
    # tiket2 = models.TiketModel.objects.all()
    test_group = Group.objects.get(name='mahasiswa')
    staf_group = Group.objects.get(name='staf')
    stafadmin_group = Group.objects.get(name='staf administrasi')
    stafnil_group = Group.objects.get(name='staf nilai')
    stafvisa_group = Group.objects.get(name='staf visa')
    user_group = request.user.groups.all()
    if test_group in user_group:
        tikets = models.TiketModel.objects.filter(mahasiswa=request.user)
    elif stafadmin_group in user_group:
        tikets = models.TiketModel.objects.filter(kategori='dokumen')
    elif stafvisa_group in user_group:
        tikets = models.TiketModel.objects.filter(kategori='visa')
    elif stafnil_group in user_group:
        tikets = models.TiketModel.objects.filter(kategori='nilai')
    else :
        tikets = models.TiketModel.objects.all()
    

    movestates = []
    for tiket in tikets:
        if staf_group in user_group:
                move = models.MoveState.objects.filter(tiket_move=tiket).exclude(state_move=1)
        else :
            move = models.MoveState.objects.filter(tiket_move=tiket).order_by('-updated')
        if move.exists():
            movestates.append(move.first())

    # movess = len(movestates)
    # # print(movestates)
    # States1 = models.State.objects.get(code_name=1)
    # States2 = models.State.objects.get(code_name=2)
    # States3 = models.State.objects.get(code_name=3)
    # States4 = models.State.objects.get(code_name=4)
    # States5 = models.State.objects.get(code_name=5)

    # pending = 0
    # opens = 0
    # process = 0
    # finish = 0
    # closed = 0
    # for i in move:
    #     if i.state_move==States4:
    #         finish = finish+1
    #     elif i.state_move==States5:
    #         closed = closed+1
    #     elif i.state_move==States3:
    #         process = process+1
    #     elif i.state_move==States2:
    #         opens = opens+1
    #     elif i.state_move==States1:
    #         pending = pending+1


    # print(pending)
    # print(opens)
    # print(process)
    # print(finish)
    # print(closed)
    # # precentage
    # # p = int(pending/allt*100)
    # # o = int(opens/allt*100)
    # # pr = int(process/allt*100)
    # # f = int(finish/allt*100)
    # c = int(closed/allt*100)

    test_group = Group.objects.get(name='mahasiswa')
    user_group = request.user.groups.all()
    if test_group in user_group:
        context = {'segment': 'index',
            'tiket_list':movestates,
            # 'pending':pending,
            # 'open':opens,
            # 'process':process,
            # 'finish':finish,
            # 'closed':closed,
            # 'allt':allt,
            # 'p':p,
            # 'o':o,
            # 'pr':pr,
            # 'f':f,
            # 'c':c,
        }
    else:
        context = {'segment': 'index',
            'tiket_list':movestates,
            # 'pending':pending,
            # 'open':opens,
            # 'process':process,
            # 'finish':finish,
            # 'closed':closed,
            # 'allt':allt,
            # 'p':p,
            # 'o':o,
            # 'pr':pr,
            # 'f':f,
            # 'c':c,
        }
    
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
