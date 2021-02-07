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
    path("<int:listing_id>/close", views.close, name="close")
]
