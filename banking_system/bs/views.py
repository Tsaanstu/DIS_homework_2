from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bs.models import User, Client, Account, History_of_changes, Transfer, Rate, IdClientData
import sqlite3
from django.http import HttpResponse

def paginator(user_list, request):
    paginator = Paginator(user_list, 15)

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


def conversion(request):
    first_id = request.GET["outgoing_account_num"]
    second_id = request.GET["incoming_account_num"]

    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    cursor.execute("SELECT currency FROM bs_account WHERE id = ?", (first_id,))
    first_cur = cursor.fetchall()[0][0]
    cursor.execute("SELECT currency FROM bs_account WHERE id = ?", (second_id,))
    second_cur = cursor.fetchall()[0][0]

    koef = 1
    if (first_cur != second_cur):
        cursor.execute("SELECT cost FROM bs_rate WHERE source_currency = ? AND final_currency = ?", (first_cur, second_cur,))
        koef = float(cursor.fetchall()[0][0])

    return HttpResponse(koef, content_type='text/html')


def transfer(request, id):
    if request.method == "POST":
        print("value is ", end="")
        print(request.POST["outgoing_account_num"])
    db_accounts = Account.objects.all().filter(cl_id=id)
    accounts = list()
    for i in db_accounts:
        client_name = Client.objects.get(pk=id)
        client_name = str(client_name.full_name)
        accounts.append(IdClientData(i.id, client_name, "Счёт №" + str(i.id) + ", дата обновления: " + str(
            i.update_time) + "; валюта: " + str(i.currency) + ", " + str(i.balance)))
    return render(request, 'bs/transfer.html', {"accounts": accounts})


def client_data(request, id):
    if request.method == "POST":
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        input_data = [(request.POST["InputLogin"], request.POST["InputTel"], request.POST["InputAddress"], id)]
        cursor.executemany("UPDATE bs_client SET login=?, tel=?, address=? WHERE id=?", input_data)
        conn.commit()

    client_data = Client.objects.get(pk=id)
    client_data.birthday = str(client_data.birthday)
    client_data.date_conclusion = str(client_data.date_conclusion)
    return render(request, 'bs/client_data.html', {"client_data": client_data})


def report(request, id):
    db_accounts = Account.objects.all().filter(cl_id=id)
    accounts = list()
    for i in db_accounts:
        client_name = Client.objects.get(pk=id)
        client_name = str(client_name.full_name)
        accounts.append(IdClientData(i.id, client_name, "Счёт №" + str(i.id) + ", дата обновления: " + str(i.update_time) + "; валюта: " + str(i.currency) + ", " + str(i.balance)))

    return render(request, 'bs/report.html', {"accounts": accounts})
