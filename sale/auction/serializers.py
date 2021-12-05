from rest_framework import serializers
from .models import  BidModel,  CommentModel, ListingModel, User, WinnerModel
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token



class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')

        def create(self, validated_data):
            if validated_data.get['password']:
                validated_data['password'] = make_password(validated_data['password'])

            user = User.objects.create(**validated_data)
            token = Token.objects.create(user = user)
            # for user in User.objects.all():
            #     Token.objects.get_or_create(user=user)
            return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self,data):
        username = data.get("username", None)
        password = data.get("password", None)
        
        try:
            user = User.objects.get(username = username, password = password)
        except:
            raise serializers.ValidationError('A user with this email and password is not found.')
        return user


class ListingSerializer(serializers.ModelSerializer):
    # image_file = serializers.CharField()

    class Meta:
        model = ListingModel
        fields = "__all__"
    # def __init__(self, *args, **kwargs):
    #     # Don't pass the 'fields' arg up to the superclass
    #     fields = kwargs.pop('fields', None)

    #     # Instantiate the superclass normally
    #     super(ListingSerializer, self).__init__(*args, **kwargs)

    #     if fields is not None:
    #         # Drop any fields that are not specified in the `fields` argument.
    #         allowed = set(fields)
    #         existing = set(self.fields)
    #         for field_name in existing - allowed:
    #             self.fields.pop(field_name)

class BidSerializer(serializers.ModelSerializer):

    class Meta:
        model = BidModel
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = "__all__"   

class WinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WinnerModel
        fields = "__all__"