from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bs.models import User, Client, Account, History_of_changes, Transfer, Rate

def paginator(user_list, request):
    paginator = Paginator(user_list, 10)

    page = request.GET.get('page')
    try:
        user_list = paginator.page(page)
    except PageNotAnInteger:
        user_list = paginator.page(1)
    except EmptyPage:
        user_list = paginator.page(paginator.num_pages)
    return user_list


def index(request):
    user_list = Client.objects.all().order_by('full_name')
    user_list = paginator(user_list, request)
    return render(request, 'bs/index.html', {"users": user_list})


def login(request):
    return render(request, 'bs/login.html', {})
