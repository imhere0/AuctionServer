from django.urls import path



from .views import ClosedListing, Register, Login, Listing, DetailView, Bid, Comment,  Winner, ActiveListing
from django import urls
 
urlpatterns = [
    path('register',Register.as_view(), name = "register"),
    path('login',Login.as_view(), name = "login"),
    path('goods', Listing.as_view(), name = 'goods' ),
    path('goods/<int:pk>',DetailView.as_view(), name = "detail"),
    path('goods/bid/<int:listingid>', Bid.as_view(), name = "bid"),
    path('goods/comments/<int:listingid>', Comment.as_view(), name = "comment" ),
    path('goods/winner/<int:listingid>', Winner.as_view(), name = "winner"),
    path('goods/closedlisting', ClosedListing.as_view(), name = "closedlisting"),
    path('goods/activelisting', ActiveListing.as_view(), name = "activelisting")
    
]