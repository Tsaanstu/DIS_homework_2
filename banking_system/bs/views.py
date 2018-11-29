from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bs.models import User, Client, Account, History_of_changes, Transfer, Rate
import sqlite3
from django.http import HttpResponse

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
    client_list = Client.objects.all().order_by('full_name')
    client_list = paginator(client_list, request)
    return render(request, 'bs/index.html', {"clients": client_list})


def login(request):
    return render(request, 'bs/login.html', {})


def report(request, id):
    return render(request, 'bs/report.html', {})


def transfer(request, id):
    return render(request, 'bs/transfer.html', {})


def client_data(request, id):
    if request.method == "POST":
        print(request.POST["InputLogin"])
        print(request.POST["InputTel"])
        print(request.POST["InputAddress"])

        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        input_data = [(request.POST["InputLogin"], request.POST["InputTel"], request.POST["InputAddress"], id)]
        cursor.executemany("UPDATE bs_client SET login=?, tel=?, address=? WHERE id=?", input_data)
        conn.commit()

    client_data = Client.objects.get(pk=id)
    client_data.birthday = str(client_data.birthday)
    client_data.date_conclusion = str(client_data.date_conclusion)
    return render(request, 'bs/client_data.html', {"client_data": client_data})
