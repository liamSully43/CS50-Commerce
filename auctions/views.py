from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
import datetime

from .models import Listing, Bid, Comment, User


def index(request):
    listings = Listing.objects.all()
    current_time_date = f"{datetime.datetime.now().date()} {datetime.datetime.now().time()}"
    active_listings = listings.filter(end_time_date__gt=current_time_date)
    return render(request, "auctions/index.html", {'listings' : active_listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def categories(request):
    current_time_date = f"{datetime.datetime.now().date()} {datetime.datetime.now().time()}" # get the current time & date
    listings = Listing.objects.all() # get all listings
    categories = []
    filtered_listings = []
    for listing in listings:
        if listing.category not in categories: # for each listing, add the listings category if is not already in the categories list
            categories.append(listing.category)
    if request.method == "POST":
        filtered_listings = listings.filter(category=request.POST["category"], end_time_date__gt=current_time_date) # filter out closed listings
    return render(request, "auctions/categories.html", {'categories': categories, 'listings': filtered_listings, 'length': len(filtered_listings)})

def createListing(request):
    # if the user is creating a new listing
    if request.method == "POST":
        start_time_date = f"{datetime.datetime.now().date()} {datetime.datetime.now().time()}" # time the listing was created
        end_time_date = f"{request.POST['end_date_year']}-{request.POST['end_date_month']}-{request.POST['end_date_day']} {request.POST['end_time']}" # user submitted closing time
        listing = Listing(
            title=request.POST["title"],
            description=request.POST["description"],
            starting_bid=request.POST["starting_bid"],
            current_bid=request.POST["starting_bid"],
            image=request.POST["image"],
            category=request.POST["category"],
            start_time_date=start_time_date,
            end_time_date=end_time_date
        )
        listing.save()
        new_listing = Listing.objects.get(title=listing.title) # get the listing just created so that the id can be accessed
        user = User.objects.get(pk=request.user.id)
        user.listings.add(new_listing) # associate the listing with the user
        return HttpResponseRedirect(f"/listing/{new_listing.id}")
    # if the user is viewing the create listings page
    else:
        class NewListingForm(forms.Form):
            title = forms.CharField(label="Title", max_length=64)
            description = forms.CharField(label="Description", widget=forms.Textarea, max_length=500)
            starting_bid = forms.IntegerField(label="Starting Bid", min_value=0)
            image = forms.CharField(label="Photo", max_length=1000)
            category = forms.CharField(label="Category", max_length=64)
            end_date = forms.DateTimeField(label="End Date of Listing", widget=forms.SelectDateWidget)
            end_time = forms.TimeField(label="Time Listing Closes", widget=forms.TextInput(attrs={"placeholder": "e.g. 17:15"}))

        return render(request, "auctions/create-listing.html", {'form' : NewListingForm})    
    
def get_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    comments = listing.comments.all()
    on_watchlist = False
    listing_owner = False
    if request.user.id != None: # is the user signed in
        # get the user's watchlist and filter by this listing's id
        watchlist = User.objects.get(pk=request.user.id).watchlist.filter(pk=listing_id)
        if len(watchlist) > 0:
            on_watchlist = True
        
        # check if the user is the owner of the listing
        users_listings = User.objects.get(pk=request.user.id).listings.filter(pk=listing_id)
        print(users_listings)
        if len(users_listings) > 0:
            listing_owner = True
    
    # check if the listing is active or not
    current_time = f"{datetime.datetime.now().date()} {datetime.datetime.now().time()}"
    end_time = str(listing.end_time_date)
    active = False
    winner = False
    if current_time < end_time:
        active = True
    else:
        # check if the current user is the highest bidder
        highest_bid = Bid.objects.get(listing=int(listing_id), value=int(listing.current_bid))
        if int(highest_bid.user) == int(request.user.id):
            winner = True

    class NewCommentForm(forms.Form):
        comment = forms.CharField(label="Comment", widget=forms.Textarea(attrs={"placeholder": "Add a comment"}), max_length=500)

    # the bid form is added using HTML instead of Python because it only has one field which has loads of attributes     
    return render(request, "auctions/listing.html", {'listing': listing, 'comments': comments, 'active': active, 'winner': winner, 'listing_owner': listing_owner, 'on_watchlist': on_watchlist, 'comment_form': NewCommentForm})
    
def watchlist(request):
    # if the user is adding/removing a listing from their watchlist
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        if request.POST["toggle"] == "add":
            listing = Listing.objects.get(pk=int(listing_id))
            person = User.objects.get(pk=int(request.user.id))
            person.watchlist.add(listing)
        else:
            listing = Listing.objects.get(pk=listing_id)
            user = User.objects.get(pk=int(request.user.id))
            user.watchlist.remove(listing)
        return HttpResponseRedirect(f"/listing/{listing_id}")
    # if the user is just viewing their watchlist page
    else:
        user = User.objects.get(pk=request.user.id)
        watchlist = user.watchlist.all()
        return render(request, "auctions/watchlist.html", {'listings' : watchlist})

def comment(request):
    # if the user is adding a new comment
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        date = datetime.datetime.now().date()
        new_comment = Comment(
            name = request.user.username,
            comment = request.POST["comment"],
            time_date = date
        )
        new_comment.save()
        comment = Comment.objects.get(comment=new_comment.comment) # get the comment just created to access the comment's id
        person = User.objects.get(pk=int(request.user.id))
        person.comments.add(comment) # associate the user with the comment
        listing = Listing.objects.get(pk=int(listing_id))
        listing.comments.add(comment) # associate the listing with the comment
        return HttpResponseRedirect(f"/listing/{listing_id}")
    # if the user is trying to visit /comment directory
    else:
        return HttpResponseRedirect("/")

def bid(request, bid_id):
    # if the user is biding on a listing
    if request.method == "POST":
        listing = Listing.objects.get(pk=int(bid_id))
        bid = int(request.POST["bid"])
        listing.current_bid = bid
        listing.save()
        new_bid = Bid(
            listing = int(listing.id),
            user = int(request.user.id),
            value = int(bid)
        )
        new_bid.save()
        return HttpResponseRedirect(f"/listing/{listing.id}")
    # if the user trys to visit /bid/<listing-id> redirect them to that listing
    else:
        return HttpResponseRedirect(f"/listing/{bid_id}")

def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=int(listing_id))
    # close the listing by setting the end time & date to the current time & date 
    listing.end_time_date = f"{datetime.datetime.now().date()} {datetime.datetime.now().time()}"
    listing.save()
    return HttpResponseRedirect(f"/listing/{listing.id}")