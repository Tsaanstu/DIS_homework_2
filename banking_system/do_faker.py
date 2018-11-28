# -*- coding: utf-8 -*-
from datetime import datetime, date, time
from faker import Factory
import sqlite3

def FAKE_CLIENT():
	MAX = 115
	conn = sqlite3.connect("db.sqlite3")
	cursor = conn.cursor()
	for i in range(0, MAX):
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

FAKE_CLIENT()
