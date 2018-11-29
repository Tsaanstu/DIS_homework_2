# -*- coding: utf-8 -*-
from datetime import datetime, date, time
from faker import Factory
import sqlite3
import random

MAX_CLIENT = 115
CLIENT_START_ID = 1
CLIETN_AND_ID = 115
NUM_ACCOUNT = 3

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
		date_conclusion = date.today()
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
			print(input_data)
			cursor.executemany('INSERT INTO bs_account (update_time, currency, balance, cl_id_id) VALUES (?, ?, ?, ?)', input_data)
	conn.commit()

FAKE_ACCOUNT()