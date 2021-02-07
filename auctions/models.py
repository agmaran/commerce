from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import BooleanField


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.FloatField(max_length=None)
    image = models.URLField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="my_listings")
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.CASCADE, related_name="category_listings")
    watchers = models.ManyToManyField(
        User, blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    amount = models.FloatField(max_length=None)
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="my_bids")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="listing_bids", default=1)

    def __str__(self):
        return f"{self.bidder} bid: {self.amount}"


class Comment(models.Model):
    comment = models.CharField(max_length=64)
    commentator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="my_comments")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="listing_comments", default=1)

    def __str__(self):
        return f"{self.commentator}: {self.comment}"
