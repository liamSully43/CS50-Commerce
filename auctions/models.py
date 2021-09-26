from django.contrib.auth.models import AbstractUser
from django.db import models

class Bid(models.Model):
    id = models.IntegerField(primary_key=True)
    listing = models.IntegerField()
    user = models.IntegerField()
    value = models.IntegerField()

    def __str__(self):
        return f"bid {self.id}"

class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    comment = models.CharField(max_length=500)
    time_date = models.DateTimeField()

    def __str__(self):
        return self.comment

class Listing(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    starting_bid = models.IntegerField()
    current_bid = models.IntegerField()
    image = models.CharField(max_length=1000)
    category = models.CharField(max_length=64)
    comments = models.ManyToManyField(Comment, blank=True, related_name="listing_comments")
    start_time_date = models.DateTimeField()
    end_time_date = models.DateTimeField()

    def __str__(self):
        return self.title

class User(AbstractUser):
    id = models.IntegerField(primary_key=True)
    listings = models.ManyToManyField(Listing, blank=True, related_name="user_listings")
    bids = models.ManyToManyField(Bid, blank=True, related_name="user_bids")
    comments = models.ManyToManyField(Comment, blank=True, related_name="user_comment")
    watchlist = models.ManyToManyField(Listing, blank=True, related_name="user_watchlist")

    def __str__(self):
        return self.username