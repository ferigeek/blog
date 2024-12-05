from rest_framework.response import Response
from rest_framework import views
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from . import models
from . import serializers
from . import permissions
from . import filters



@extend_schema(
    parameters=[
        OpenApiParameter(
            name='mine',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description='Filter posts authored by the current user',
            required=False,
            default=False
        ),
    ]
)
class PostsView(generics.ListCreateAPIView):
    permission_classes= [permissions.GetPostPermission]
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostsSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = filters.PostFilter
    search_fields = ['title', 'content', 'author__first_name', 'author__last_name', 'category__name']
    ordering_fields = ['title', 'author__first_name', 'author__last_name', 'category__name', 'publish_date', 'view_count']

    def get_queryset(self):
        queryset = models.Post.objects.all()
        mine = self.request.query_params.get('mine', None)

        if mine and mine.lower() == 'true':
            queryset = queryset.filter(author=self.request.user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, view_count=0)



class PostView(views.APIView):
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.EditingPermission]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request, id, *args, **kwargs):
        try:
            post = models.Post.objects.get(pk=id)
        except models.Post.DoesNotExist:
            raise NotFound("Post not found!")

        serializer = serializers.PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id, *args, **kwargs):
        try:
            post = models.Post.objects.get(pk=id)
        except models.Post.DoesNotExist:
            raise NotFound(detail="Post not found!")
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def handle_put_patch(self, request, is_patch):
        try:
            post = models.Post.objects.get(pk=id)
        except models.Post.DoesNotExist:
            raise NotFound("Post not found!")
        
        author = request.data.get('author')
        if author:
            if author != post.author:
                return Response({"error": "You can't change the \"author\""}, status=status.HTTP_403_FORBIDDEN)
        view_count = request.data.get('view_count')
        if view_count:
            if view_count != post.view_count:
                return Response({"error": "You can't change the \"view_count\""}, status=status.HTTP_403_FORBIDDEN)
        publish_date = request.data.get('publish_date')
        if publish_date:
            if publish_date != post.publish_date:
                return Response({"error": "You can't change the \"publish_date\""}, status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.PostSerializer(post, data=request.data, partial=is_patch)
        
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, *args, **kwargs):
        self.handle_put_patch(request, False)
        
    def patch(self, request, id, *args, **kwargs):
        self.handle_put_patch(request, False)

    def post(self, request, id, *args, **kwargs):
        try:
            post = models.Post.objects.get(pk=id)
        except models.Post.DoesNotExist:
            raise NotFound("Post not found!")
        
        post.view_count += 1
        post.save()
        return Response({"success": "View count updated!"}, status=status.HTTP_200_OK)
        


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='mine',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description='Filter comments authored by the current user',
            required=False,
            default=False
        ),
    ]
)
class PostCommentView(generics.ListAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = serializers.CommentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['content', 'author__first_name', 'author__last_name', 'post__title']
    ordering_fields = ['published_date', 'author__first_name', 'author__last_name']
    filterset_class = filters.CommentFilter

    def get_queryset(self):
        post_id = self.kwargs['id']
        try:
            post = models.Post.objects.get(pk=post_id)
        except models.Post.DoesNotExist:
            raise NotFound("Post not found!")
        queryset = models.Comment.objects.filter(post=post)
        
        mine = self.request.query_params.get('mine', None)
        if mine and mine.lower() == 'true':
            queryset = queryset.filter(author=self.request.user)
        return queryset



@extend_schema(
    parameters=[
        OpenApiParameter(
            name='mine',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description='Filter comments authored by the current user',
            required=False,
            default=False
        ),
    ]
)
class CommentsView(generics.ListCreateAPIView):
    permission_classes= [permissions.GetPostPermission]
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['content', 'author__first_name', 'author__last_name', 'post__title']
    ordering_fields = ['published_date', 'author__first_name', 'author__last_name']
    filterset_class = filters.CommentFilter

    def get_queryset(self):
        queryset = models.Comment.objects.all()
        mine = self.request.query_params.get('mine', None)
        if mine and mine.lower() == 'true':
            queryset = queryset.filter(author=self.request.user)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class CommentView(views.APIView):
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.EditingPermission]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request, id, *args, **kwargs):
        try:
            comment = models.Comment.objects.get(pk=id)
        except models.Comment.DoesNotExist:
            raise NotFound("Comment not found!")

        serializer = serializers.CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id, *args, **kwargs):
        try:
            comment = models.Comment.objects.get(pk=id)
        except models.Comment.DoesNotExist:
            raise NotFound(detail="Comment not found!")
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def handle_put_patch(self, request, is_patch):
        try:
            comment = models.Comment.objects.get(pk=id)
        except models.Comment.DoesNotExist:
            raise NotFound("Comment not found!")
        
        author = request.data.get('author')
        if author:
            if author != comment.author:
                return Response({"error": "You can't change the \"author\""}, status=status.HTTP_403_FORBIDDEN)
        published_date = request.data.get('published_date')
        if published_date:
            if published_date != comment.published_date:
                return Response({"error": "You can't change the \"published_date\""}, status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.CommentSerializer(comment, data=request.data, partial=is_patch)
        
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, *args, **kwargs):
        self.handle_put_patch(request, False)
        
    def patch(self, request, id, *args, **kwargs):
        self.handle_put_patch(request, False)



class CategoriesView(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
