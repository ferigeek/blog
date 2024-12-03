from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, throttle_classes
from rest_framework import status
from . import models
from . import serializers


@api_view(['GET'])
def getPostsView(request):
    """Returns all the posts"""
    posts = models.Post.objects.all()
    ser_posts = serializers.PostsSerializer(posts, many=True)
    return Response(ser_posts.data)


@api_view(['POST'])
def createPostView(request):
    """
    Creates a new post in the blog.

    Fields:
        - title (str): The title of the post. Max length: 20 characters.
        - content (str): The content of the post. Can be a long text.
        - author (int): The ID of the user creating the post (foreign key).
        - publish_date (str): The publish date in ISO format (e.g., "2024-12-03T00:00:00Z").
        - category (int, optional): The ID of the category the post belongs to. If not provided, it will be left empty.

    Returns:
        Response:
            - On success: The created post details with HTTP status code 201.
            - On failure: Error message detailing the validation issues with HTTP status code 400.

    """
    ser_post = serializers.PostsSerializer(data=request.data)
    
    if ser_post.is_valid():
        ser_post.save()
        return Response(ser_post.data, status=status.HTTP_201_CREATED)
    
    return Response(ser_post.errors, status=status.HTTP_400_BAD_REQUEST)