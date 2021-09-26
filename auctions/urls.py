from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("create-listing", views.createListing, name="createListing"),
    path("listing/<str:listing_id>", views.get_listing, name="viewListing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("comment", views.comment, name="comment"),
    path("bid/<str:bid_id>", views.bid, name="bid"),
    path("close-listing/<str:listing_id>", views.close_listing, name="close")
]