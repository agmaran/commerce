from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models.deletion import SET_NULL
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, Listing, Bid
from django import forms
from django.contrib.auth.decorators import login_required


class NewListingForm(forms.Form):
    title = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    description = forms.CharField(
        required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'size': '20'}))
    price = forms.FloatField(required=True, label="Starting bid", widget=forms.NumberInput(
        attrs={'class': 'form-control'}))
    image = forms.URLField(required=False, label="Image URL", empty_value="https://ctkbiotech.com/wp/wp-content/uploads/2018/03/not-available.jpg",
                           widget=forms.URLInput(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(required=False, queryset=Category.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control'}))


class PlaceBidForm(forms.Form):
    bid = forms.FloatField(required=True, label="Your bid",
                           widget=forms.NumberInput(attrs={'class': 'form-control'}))


def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.filter(active=True)
    })


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


def create(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            l = Listing(title=form.cleaned_data["title"], description=form.cleaned_data["description"], price=form.cleaned_data["price"],
                        image=form.cleaned_data["image"], owner=request.user, category=form.cleaned_data["category"])
            l.save()
        else:
            return render(request, "auctions/create.html", {
                'form': form
            })
    return render(request, "auctions/create.html", {
        'form': NewListingForm()
    })


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        form = PlaceBidForm(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                if (form.cleaned_data["bid"] > listing.price):
                    b = Bid(amount=form.cleaned_data["bid"],
                            bidder=request.user, listing=listing)
                    b.save()
                    listing.price = form.cleaned_data["bid"]
                    listing.save()
                else:
                    try:
                        is_on_watchlist = listing in request.user.watchlist.all()
                    except AttributeError:
                        is_on_watchlist = False
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "n_bids": len(listing.listing_bids.all()),
                        "is_on_watchlist": is_on_watchlist,
                        "my_bids": request.user.my_bids.filter(listing=listing),
                        "form": form,
                        "error": "The bid must be greater than the current price for the listing."
                    })
            else:
                try:
                    is_on_watchlist = listing in request.user.watchlist.all()
                except AttributeError:
                    is_on_watchlist = False
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "n_bids": len(listing.listing_bids.all()),
                    "is_on_watchlist": is_on_watchlist,
                    "my_bids": request.user.my_bids.filter(listing=listing),
                    "form": form
                })
        else:
            return HttpResponseRedirect(reverse("login"))
    try:
        is_on_watchlist = listing in request.user.watchlist.all()
        my_bids = request.user.my_bids.filter(listing=listing)
    except:
        is_on_watchlist = False
        my_bids = None
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "n_bids": len(listing.listing_bids.all()),
        "is_on_watchlist": is_on_watchlist,
        "my_bids": my_bids,
        "form": PlaceBidForm()
    })


@login_required(login_url="login")
def a_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.watchers.add(request.user)
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


def r_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    request.user.watchlist.remove(listing)
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))
