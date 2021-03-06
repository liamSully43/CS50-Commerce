# Generated by Django 3.2.5 on 2021-09-04 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing', models.IntegerField()),
                ('user', models.IntegerField()),
                ('bid', models.IntegerField()),
                ('time_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('comment', models.CharField(max_length=500)),
                ('time_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=500)),
                ('starting_bid', models.IntegerField()),
                ('current_bid', models.IntegerField()),
                ('image', models.CharField(max_length=1000)),
                ('category', models.CharField(max_length=64)),
                ('start_time_date', models.DateTimeField()),
                ('end_time_date', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='bids',
            field=models.ManyToManyField(blank=True, related_name='user_bids', to='auctions.Bid'),
        ),
        migrations.AddField(
            model_name='user',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='user_comment', to='auctions.Comment'),
        ),
        migrations.AddField(
            model_name='user',
            name='listings',
            field=models.ManyToManyField(blank=True, related_name='user_listings', to='auctions.Listing'),
        ),
    ]
