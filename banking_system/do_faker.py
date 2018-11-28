# -*- coding: utf-8 -*-
from faker import Factory
import codecs
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from bs.models import Client
from random import choice, randint
import urllib.request as request
from django.core.files import File


class Command(BaseCommand):
    help = 'Fills database with fake data'
    faker = Factory.create()

    CLIENT_COUNT = 0

    def add_arguments(self, parser):
        pass

    def create_client(self):
        for i in range(0, self.CLIENT_COUNT):
            profile = self.faker.profile()
            u = Client()
            u.full_name = profile['name']
            u.login = profile['username']
            u.birthday = profile['birthdate']
            u.contract_number = profile['ssn']
            u.date_conclusion = self.faker.phone_number()
            u.tel = self.faker.past_datetime()
            u.addtess = profile['address']
            u.save()

            self.stdout.write('[%d] added user %s' % (u.id, u.username))

    def handle(self, *args, **options):
        self.create_client()

