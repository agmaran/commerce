from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:listing_id>/listing", views.listing, name="listing"),
    path("<int:listing_id>/a_watchlist", views.a_watchlist, name="a_watchlist"),
    path("<int:listing_id>/r_watchlist", views.r_watchlist, name="r_watchlist"),
    path("<int:listing_id>/close", views.close, name="close"),
    path("<int:listing_id>/comment", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("<int:category_id>/category", views.category, name="category"),
    path("my_listings", views.my_listings, name="my_listings")
]
