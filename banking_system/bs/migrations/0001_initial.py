# Generated by Django 2.1.3 on 2018-11-25 12:51

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('upload', models.ImageField(upload_to='uploads/%Y/%m/%d/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_time', models.DateField()),
                ('currency', models.CharField(max_length=3)),
                ('balance', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=30)),
                ('login', models.CharField(max_length=20)),
                ('birthday', models.DateField()),
                ('contract_number', models.CharField(max_length=10)),
                ('date_conclusion', models.DateField()),
                ('tel', models.CharField(max_length=12)),
                ('address', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='History_of_changes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_balance', models.FloatField()),
                ('new_balance', models.FloatField()),
                ('reason', models.CharField(max_length=30)),
                ('update_time', models.DateField()),
                ('acc_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bs.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_currency', models.CharField(max_length=3)),
                ('final_currency', models.CharField(max_length=3)),
                ('cost', models.FloatField()),
                ('update', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tr_date', models.DateField()),
                ('source_currency', models.CharField(max_length=3)),
                ('source_sum', models.FloatField()),
                ('final_currency', models.CharField(max_length=3)),
                ('final_sum', models.FloatField()),
                ('final_his_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='final_his_id', to='bs.History_of_changes')),
                ('source_his_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_his_id', to='bs.History_of_changes')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='cl_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bs.Client'),
        ),
    ]
