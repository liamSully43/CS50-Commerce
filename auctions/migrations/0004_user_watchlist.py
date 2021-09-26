# Generated by Django 3.2.7 on 2021-09-12 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210905_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='user_watchlist', to='auctions.Listing'),
        ),
    ]
