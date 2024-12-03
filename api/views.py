from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers


@api_view(['GET', 'POST'])
def postsView(request):
    if request.method == 'GET':
        posts = models.Post.objects.all()
        ser_posts = serializers.PostsSerializer(posts, many=True)
        return Response(ser_posts.data)
    

    elif request.method == 'POST':
        ser_post = serializers.PostsSerializer(data=request.data)
        if ser_post.is_valid():
            ser_post.save()
            return Response(ser_post.data, status=status.HTTP_201_CREATED)
        return Response(ser_post.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'DELETE', 'PUT', 'PATCH', 'POST'])
def postView(request, id):
    if request.method == 'GET':
        try:
            post = models.Post.objects.get(pk=id)
        except models.Post.DoesNotExist:
            raise NotFound(detail='Post not found!')
        
        ser_post = serializers.PostSerializer(post)

        return Response(ser_post.data)
    

    if request.method == 'DELETE':
        try:
            post = models.Post.objects.get(pk=id)
        except models.Post.DoesNotExist:
            raise NotFound(detail="Post not found!")
        
        if post.author == request.user or request.user.is_staff:
            post.delete()
            return Response(
                {"success": "Post successfully deleted!"}, 
                status=status.HTTP_204_NO_CONTENT
                )

        return Response(
            {"error": "You do not have permission to delete this post!"}, 
            status=status.HTTP_403_FORBIDDEN
            )
    

    if request.method == 'PUT' or request.method == 'PATCH':
        try:
            post = models.Post.objects.get(pk=id)
        except models.Post.DoesNotExist:
            raise NotFound("Post not found!")
        
        if request.user == post.author or request.user.is_staff:
            ser_post = serializers.PostSerializer(
                post, 
                data=request.data, 
                partial=(request.method == 'PATCH')
                )
            
            if ser_post.is_valid():
                ser_post.save()
                return Response({"success":"Successfully modifed post!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Bad request!"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(
            {"error": "You do not have permission to delete this post!"}, 
            status=status.HTTP_403_FORBIDDEN
            )
    

    if request.method == 'POST':
        try:
            post = models.Post.objects.get(pk=id)
        except models.Post.DoesNotExist:
            raise NotFound("Post not found!")
        
        post.view_count += 1
        post.save()
        post.refresh_from_db()

        return Response(
            {"success": "view count updated!", "view_count": post.view_count}, 
            status=status.HTTP_200_OK
            )
    



@api_view(['GET'])
def getCommentOfPostView(request, id):
    try:
        post = models.Post.objects.get(pk=id)
    except models.Post.DoesNotExist:
        raise NotFound("Post not found!")
    
    comment = models.Comment.objects.filter(post=post)
    ser_comment = serializers.CommentSerializer(comment, many=True)
    
    return Response(ser_comment.data, status=status.HTTP_200_OK)
