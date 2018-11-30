# -*- coding: utf-8 -*-
from datetime import datetime, date, time
from faker import Factory, Faker
import sqlite3
import random

MAX_CLIENT = 200
CLIENT_START_ID = 1
CLIETN_AND_ID = 200
NUM_ACCOUNT = 3
TRANSFER_NUM = 2000

CURRENCY = ["RUB", "USD", "EUR"]


def FAKE_CLIENT():
	conn = sqlite3.connect("db.sqlite3")
	cursor = conn.cursor()
	for i in range(0, MAX_CLIENT):
		faker = Factory.create()
		profile = faker.profile()
		full_name = profile['name']
		login = profile['username']
		birthday = profile['birthdate']
		contract_number = hash(login + str(birthday)) 
		if contract_number < 0:
			contract_number *= -1
		date_conclusion = faker.date_time_between(start_date="-10y", end_date="-5y", tzinfo=None).date()
		tel = '+79999999999'
		address = 'Moscow'
		input_data = [(full_name, login, birthday, contract_number, date_conclusion, tel, address)]
		cursor.executemany('INSERT INTO bs_client (full_name, login, birthday, contract_number, date_conclusion, tel, address) VALUES (?, ?, ?, ?, ?, ?, ?)', input_data)
	conn.commit()


def FAKE_ACCOUNT():
	conn = sqlite3.connect("db.sqlite3")
	cursor = conn.cursor()
	for i in range(CLIENT_START_ID, CLIETN_AND_ID + 1):
		for j in range(0, NUM_ACCOUNT):
			update_time = date.today()
			currency = CURRENCY[random.randint(0, 2)]
			balance = random.randint(0, 100000)
			cl_id_id = i
			input_data = [(update_time, currency, balance, cl_id_id)]
			cursor.executemany('INSERT INTO bs_account (update_time, currency, balance, cl_id_id) VALUES (?, ?, ?, ?)', input_data)
	conn.commit()


def FAKE_TRANSFER():
	for i in range(0, TRANSFER_NUM):
		make_a_transfer()


def history_of_changes(old_balance, new_balance, reason, update_time, acc_id):
	conn = sqlite3.connect("db.sqlite3")
	cursor = conn.cursor()
	cursor.execute('INSERT INTO bs_history_of_changes (old_balance, new_balance, reason, update_time, acc_id_id) VALUES (?, ?, ?, ?, ?)', (old_balance, new_balance, reason, update_time, acc_id))
	conn.commit()
	return int(cursor.lastrowid)

def make_a_transfer():
	faker = Factory.create()
	conn = sqlite3.connect("db.sqlite3")
	cursor = conn.cursor()
	first_id = random.randint(1, MAX_CLIENT * NUM_ACCOUNT)
	second_id = random.randint(1, MAX_CLIENT * NUM_ACCOUNT)

	while first_id == second_id:
		second_id = random.randint(1, MAX_CLIENT * NUM_ACCOUNT)

	cursor.execute("SELECT currency FROM bs_account WHERE id = ?", (first_id,))
	first_cur = cursor.fetchall()[0][0]
	cursor.execute("SELECT currency FROM bs_account WHERE id = ?", (second_id,))
	second_cur = cursor.fetchall()[0][0]

	cursor.execute("SELECT balance FROM bs_account WHERE id = ?", (first_id,))
	first_old_sum = float(cursor.fetchall()[0][0])
	cursor.execute("SELECT balance FROM bs_account WHERE id = ?", (second_id,))
	second_old_sum = float(cursor.fetchall()[0][0])

	transfer_sum = float(random.randint(1, first_old_sum))
	first_new_sum = first_old_sum - transfer_sum

	koef = 1
	if (first_cur != second_cur):
		cursor.execute("SELECT cost FROM bs_rate WHERE source_currency = ? AND final_currency = ?", (first_cur, second_cur,))
		koef = float(cursor.fetchall()[0][0])
	second_new_sum = second_old_sum + transfer_sum * koef

	date = faker.date_time_between(start_date="-2y", end_date="now", tzinfo=None).date()

	first_hid_id = history_of_changes(first_old_sum, first_new_sum, "transfer", date, first_id)
	second_hid_id = history_of_changes(second_old_sum, second_new_sum, "transfer", date, second_id)

	cursor.execute(
		'INSERT INTO bs_transfer (tr_date, source_currency, source_sum, final_currency, final_sum, final_his_id_id, source_his_id_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
		(date, first_cur, transfer_sum, second_cur, transfer_sum * koef, first_hid_id, second_hid_id))
	conn.commit()

print("CLIENT")
FAKE_CLIENT()
print("ACCOUNT")
FAKE_ACCOUNT()
print("TRANSFER")
FAKE_TRANSFER()
print("END")