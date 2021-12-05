from auction.models import User
from django.contrib import admin
from .models import  BidModel, ListingModel, User, BidModel, CommentModel, WinnerModel

# Register your models here.
admin.site.register(User)
admin.site.register(ListingModel)
admin.site.register(BidModel)
admin.site.register(CommentModel)
admin.site.register(WinnerModel)