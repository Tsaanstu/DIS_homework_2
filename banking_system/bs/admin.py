from django.contrib import admin

from bs.models import User, Client, Account, History_of_changes, Transfer, Rate

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Account)
admin.site.register(History_of_changes)
admin.site.register(Transfer)
admin.site.register(Rate)
