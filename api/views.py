from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers


# /post

@api_view(['GET', 'POST'])
def postsView(request):
    if request.method == 'GET':
        posts = models.Post.objects.all()
        ser_posts = serializers.PostsSerializer(posts, many=True)
        return Response(ser_posts.data)
    

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({"error": "You do not have permission!"}, status=status.HTTP_403_FORBIDDEN)
        ser_post = serializers.PostsSerializer(data=request.data)
        if ser_post.is_valid():
            ser_post.validated_data['author'] = request.user
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
    

    elif request.method == 'DELETE':
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
    

    elif request.method == 'PUT' or request.method == 'PATCH':
        try:
            post = models.Post.objects.get(pk=id)
        except models.Post.DoesNotExist:
            raise NotFound("Post not found!")
        
        if request.user == post.author or request.user.is_staff:
            data = request.data.copy()
            data.pop('view_count', None)
            data.pop('author', None)
            data.pop('published_date', None)

            ser_post = serializers.PostSerializer(
                post, 
                data=data, 
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
    

    elif request.method == 'POST':
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




# /comments

@api_view(['GET', 'POST'])
def commentsView(request):
    if request.method == 'GET':
        comments = models.Comment.objects.all()
        ser_comments = serializers.CommentSerializer(comments, many=True)
        return Response(ser_comments.data, status=status.HTTP_200_OK)
    

    elif request.method == 'POST':
        if request.user.is_authenticated:
            ser_comment = serializers.CommentSerializer(data=request.data)
            if ser_comment.is_valid():
                ser_comment.validated_data['author'] = request.user
                ser_comment.save()
                return Response(ser_comment.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "You don't have permission!"}, status=status.HTTP_403_FORBIDDEN)




@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
def commentView(request, id):
    if request.method == 'GET':
        comment = models.Comment.objects.get(pk=id)
        ser_comment = serializers.CommentSerializer(comment)
        return Response(ser_comment.data, status=status.HTTP_200_OK)
    

    elif request.method == 'DELETE':
        try:
            comment = models.Comment.objects.get(pk=id)
        except models.Comment.DoesNotExist:
            raise NotFound("Comment not found!")
        
        if request.user == comment.author or request.user.is_staff:
            comment.delete()
            return Response({"success": "comment deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
        
        return Response({"error": "You don't have permission!"}, status=status.HTTP_403_FORBIDDEN)
    

    elif request.method == 'PUT' or request.method == 'PATCH':
        try:
            comment = models.Comment.objects.get(pk=id)
        except models.Comment.DoesNotExist:
            raise NotFound
        
        if request.user == comment.author or request.user.is_staff:
            data = request.data.copy()
            data.pop('post', None)
            data.pop('author', None)
            data.pop('published_date', None)

            ser_comment = serializers.CommentSerializer(
                comment,
                data=data,
                partial=(request.method == 'PATCH')
            )

            if ser_comment.is_valid():
                ser_comment.save()
                return Response({"success":"Successfully modifed post!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Bad request!"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(
            {"error": "You do not have permission to delete this post!"}, 
            status=status.HTTP_403_FORBIDDEN
            )
    



@api_view(['GET'])
def categoryView(request):
    categories = models.Category.objects.all()
    ser_cat = serializers.CategorySerializer(categories, many=True)

    return Response(ser_cat.data, status=status.HTTP_200_OK)