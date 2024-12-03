from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = '__all__'


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = models.Post
        fields = [
            'id', 
            'title', 
            'view_count', 
            'publish_date', 
            'author', 
            'category', 
            'content', 
            'comments'
            ]



class UserSerializer(UserCreateSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name']