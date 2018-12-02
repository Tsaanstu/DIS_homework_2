from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bs.models import User, Client, Account, History_of_changes, Transfer, Rate, IdClientData, Worker
import sqlite3
import datetime
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


#request.user.username
def check_admin_permisions(username):
    print("username =", username)
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM bs_user WHERE username = ?", (username,))
    id = cursor.fetchall()[0][0]
    print("id =", id)
    cursor.execute("SELECT group_id FROM bs_user_groups WHERE user_id = ?", (id,))
    if cursor.fetchall()[0][0] == 2:
        return 1
    return -1


def change_of_rate(request):
    if check_admin_permisions(request.user.username) < 0:
        return render(request, 'bs/permission_denied.html', {})
    return render(request, 'bs/change_of_rate.html', {})


def permission_denied(request):
    return render(request, 'bs/permission_denied.html', {})


def index(request):
    client_list = Client.objects.all().order_by('full_name')
    client_list = paginator(client_list, request)
    return render(request, 'bs/index.html', {"clients": client_list})


def login(request):
    return render(request, 'bs/login.html', {})


def report(request, id):
    return render(request, 'bs/report.html', {})


def history_of_changes(old_balance, new_balance, reason, update_time, acc_id):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO bs_history_of_changes (old_balance, new_balance, reason, update_time, acc_id_id) VALUES (?, ?, ?, ?, ?)',
        (old_balance, new_balance, reason, update_time, acc_id))
    conn.commit()
    return int(cursor.lastrowid)


def make_a_transfer(first_id, second_id, transfer_sum):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT currency FROM bs_account WHERE id = ?", (first_id,))
    first_cur = cursor.fetchall()[0][0]
    cursor.execute("SELECT currency FROM bs_account WHERE id = ?", (second_id,))
    second_cur = cursor.fetchall()[0][0]
    cursor.execute("SELECT balance FROM bs_account WHERE id = ?", (first_id,))
    first_old_sum = float(cursor.fetchall()[0][0])
    cursor.execute("SELECT balance FROM bs_account WHERE id = ?", (second_id,))
    second_old_sum = float(cursor.fetchall()[0][0])
    first_new_sum = first_old_sum - transfer_sum
    koef = 1
    if (first_cur != second_cur):
        cursor.execute("SELECT cost FROM bs_rate WHERE source_currency = ? AND final_currency = ?",
                       (first_cur, second_cur,))
        koef = float(cursor.fetchall()[0][0])
    second_new_sum = second_old_sum + transfer_sum * koef
    date = datetime.date.today()
    first_hid_id = history_of_changes(first_old_sum, first_new_sum, "transfer", date, first_id)
    second_hid_id = history_of_changes(second_old_sum, second_new_sum, "transfer", date, second_id)
    cursor.execute(
        'INSERT INTO bs_transfer (tr_date, source_currency, source_sum, final_currency, final_sum, final_his_id_id, source_his_id_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (date, first_cur, transfer_sum, second_cur, transfer_sum * koef, first_hid_id, second_hid_id))
    conn.commit()


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
        cursor.execute("SELECT cost FROM bs_rate WHERE source_currency = ? AND final_currency = ?",
                       (first_cur, second_cur,))
        koef = float(cursor.fetchall()[0][0])

    return HttpResponse(koef, content_type='text/html')


def transfer(request, id):
    if request.method == "POST":
        first_id = request.POST["outgoing_account_num"]
        second_id = request.POST["incoming_account_num"]
        transfer_sum = request.POST["currency_1"]
        make_a_transfer(first_id, second_id, float(transfer_sum))

    db_accounts = Account.objects.all().filter(cl_id=id)
    accounts = list()
    for i in db_accounts:
        client_name = Client.objects.get(pk=id)
        client_name = str(client_name.full_name)
        accounts.append(IdClientData(i.id, client_name, "Счёт №" + str(i.id) + ", дата обновления: " + str(
            i.update_time) + "; валюта: " + str(i.currency) + ", " + str(i.balance)))
    print(datetime.date.today())
    return render(request, 'bs/transfer.html', {"accounts": accounts})


def worker_list(request):
    if check_admin_permisions(request.user.username) < 0:
        return render(request, 'bs/permission_denied.html', {})
    worker_list = Worker.objects.all().order_by('full_name')
    print(worker_list)
    worker_list = paginator(worker_list, request)
    print(worker_list)
    return render(request, 'bs/worker_list.html', {"worker_list": worker_list})


def worker_data(request, id):
    if check_admin_permisions(request.user.username) < 0:
        return render(request, 'bs/permission_denied.html', {})
    if request.method == "POST":
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        input_data = [(request.POST["InputLogin"], request.POST["InputTel"], request.POST["InputAddress"], id)]
        cursor.executemany("UPDATE bs_worker SET login=?, tel=?, address=? WHERE id=?", input_data)
        conn.commit()

    worker_data = Worker.objects.get(pk=id)
    worker_data.birthday = str(worker_data.birthday)
    worker_data.date_conclusion = str(worker_data.date_conclusion)
    return render(request, 'bs/worker_data.html', {"worker_data": worker_data})


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


def make_a_removal(id, sum):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM bs_account WHERE id = ?", (id,))
    old_balance = cursor.fetchall()[0][0]
    date = datetime.date.today()
    if (old_balance - sum < 0):
        return 0
    history_of_changes(old_balance, old_balance - sum, "removal", date, id)
    cursor.execute('UPDATE bs_account SET balance = ? WHERE id = ?', (old_balance - sum, id))
    conn.commit()
    return 1


def error_removal(request, id):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT bs_client.id, bs_client.full_name FROM bs_account JOIN bs_client on bs_account.cl_id_id = bs_client.id WHERE bs_account.id = ?",
        (id,))
    result = cursor.fetchall()
    clients = [result[0][0], result[0][1]]
    conn.commit()
    return render(request, 'bs/error_removal.html', {"clients": clients})


def removal(request, id):
    if request.method == "POST":
        r_id = request.POST["outgoing_account_num"]
        sum = request.POST["currency_1"]
        if (make_a_removal(r_id, float(sum)) == 0):
            return error_removal(request, id)

    db_accounts = Account.objects.all().filter(cl_id=id)
    accounts = list()
    for i in db_accounts:
        client_name = Client.objects.get(pk=id)
        client_name = str(client_name.full_name)
        accounts.append(IdClientData(i.id, client_name, "Счёт №" + str(i.id) + ", дата обновления: " + str(
            i.update_time) + "; валюта: " + str(i.currency) + ", " + str(i.balance)))
    print(datetime.date.today())
    return render(request, 'bs/removal.html', {"accounts": accounts})


def make_a_replenishment(id, sum):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM bs_account WHERE id = ?", (id,))
    old_balance = cursor.fetchall()[0][0]
    date = datetime.date.today()
    history_of_changes(old_balance, old_balance + sum, "replenishment", date, id)
    print(old_balance)
    print(sum)
    cursor.execute('UPDATE bs_account SET balance = ? WHERE id = ?', (old_balance + sum, id))
    conn.commit()


def monthly_report(request, date=datetime.date.today()):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    print(date.month)
    print(date.year)
    cursor.execute(
        "SELECT * FROM bs_history_of_changes WHERE strftime('%m', update_time) = ? AND strftime('%Y', update_time) = ?",
        (str(date.month), str(date.year)))
    histories = cursor.fetchall()
    conn.commit()
    return render(request, 'bs/monthly_report.html', {"histories": histories})


def replenishment(request, id):
    if request.method == "POST":
        r_id = request.POST["outgoing_account_num"]
        sum = request.POST["currency_1"]
        make_a_replenishment(r_id, float(sum))

    db_accounts = Account.objects.all().filter(cl_id=id)
    accounts = list()
    for i in db_accounts:
        client_name = Client.objects.get(pk=id)
        client_name = str(client_name.full_name)
        accounts.append(IdClientData(i.id, client_name, "Счёт №" + str(i.id) + ", дата обновления: " + str(
            i.update_time) + "; валюта: " + str(i.currency) + ", " + str(i.balance)))
    print(datetime.date.today())
    return render(request, 'bs/replenishment.html', {"accounts": accounts})
