# Generated by Django 3.2.7 on 2021-09-18 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='time_date',
        ),
    ]
