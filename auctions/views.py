from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models.deletion import SET_NULL
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, Listing
from django import forms


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
