from re import L
from django.http.response import Http404
from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import serializers, status
from .serializers import BidSerializer, ListingSerializer, RegisterSerializer, LoginSerializer, CommentSerializer, WinnerSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import CommentModel, ListingModel, BidModel, WinnerModel
from django.contrib.auth.decorators import login_required
import base64

class Register(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        status_code = status.HTTP_201_CREATED
        token = Token.objects.get_or_create(user=user)
        return Response({
            
            "message":"User Registered sucessfully",
            "status": status_code,
            
        }
        )

class Login(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
           
        user = serializer.validated_data
        return Response({
            "message":"User logged in sucessfully.",
            "token": Token.objects.get(user = user).key,
            "username": user.username,
            "user_id": user.id,
        })

class Listing(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ListingSerializer

    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        listings = ListingModel.objects.all()
             
        serializer = ListingSerializer(listings, many = True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        
        serializer = ListingSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(request.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
class DetailView(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self,pk):
        try:

            return ListingModel.objects.get(pk = pk)
        except:
            raise Http404
       
    def get(self, request, pk, format=None):
        listing = self.get_object(pk)
        serializer = ListingSerializer(listing)
        return Response(serializer.data)

    def change_price(self, pk, price):
        listing = self.get_object(pk)
        listing.price = price
        listing.save()
        # if (serializer.is_valid()):
        #     serializer.save()
        return None  
    @login_required
    def put(self, request,  pk, format=None, *args, **kwargs):
        listing = self.get_object(pk)
        serializer = ListingSerializer(listing, data=request.data, partial = True)
        if ((serializer.is_valid()))  :
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @login_required
    def delete(self, request, pk, format=None):
        listing = self.get_object(pk)
        listing.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class Bid(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    
    
    def filter_object(self, listingid):
        try:
            return BidModel.objects.filter(listingid = listingid)
        except:
            raise Http404
    
    def get(self, request, listingid, format = None):
        bid = self.filter_object(listingid )
        serializer = BidSerializer(bid, many = True)
        count = BidModel.objects.filter(listingid = listingid).count()
        return Response(serializer.data , count)

    
    def post(self, request, listingid, format = None):
        serializer = BidSerializer(data = request.data)
        price = request.data['amount']
        if serializer.is_valid():
            detail = DetailView()
            detail.change_price(pk = listingid, price = price )
            serializer.save()
            return Response({
            "message":"Your bid has been sucessfully entered."
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                    


class Comment(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    
    def get(self, request, listingid, format = None):
        comments = CommentModel.objects.filter(listingid = listingid)
        serializer = CommentSerializer(comments, many = True)
        return Response(serializer.data,
         )
    
    def post(self, request, listingid, format = None):
        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Successfully commented."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Winner(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, listingid, format = None):
        winner = WinnerModel.objects.get(listingid = listingid)
        serializer = WinnerSerializer(winner, many = False)
        return Response(serializer.data,)

    def post(self, request, listingid, format = None):
        serializer = WinnerSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Sucessfully closed."}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ClosedListing(APIView):
    
    def get(self,request,format = None):
        winner_list = []
        posts = []

        try:
            winnerobject = WinnerModel.objects.all()
        except:
            winnerobject = None
        
        if winnerobject:

            for element in winnerobject:
                winner_list.append(element.listingid)
                
            
            listingobject = ListingModel.objects.all()

            for item in listingobject:
                if item in winner_list:
                    posts.append(item)
            serializer = ListingSerializer(posts, many = True)

            return Response( serializer.data,
            )
        
        return Response({
            "message": "No listing has been closed."
        })

class ActiveListing(APIView):
    
    def get(self,request,format = None):
        winner_list = []
        posts = []

        try:
            winnerobject = WinnerModel.objects.all()
        except:
            winnerobject = None
        
        if winnerobject:

            for element in winnerobject:
                winner_list.append(element.listingid)
                
            
            listingobject = ListingModel.objects.all()

            for item in listingobject:
                if item not in winner_list:
                    posts.append(item)
            
            serializer = ListingSerializer(posts, many = True)

            return Response( serializer.data,
            )
        
        return Response({
            "message": "There are no more active listing."
        })
