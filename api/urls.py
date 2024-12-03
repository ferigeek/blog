"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views


urlpatterns = [
    path('posts', views.getPostsView, name='get_posts'),
    path('posts', views.createPostView, name='create_post'),
    path('posts/<int:id>', views.getPostView, name='get_post'),
    path('posts/<int:id>', views.deletePostView, name='delete_post'),
    path('posts/<int:id>', views.modifyPostView, name='modify_post'),
    path('posts/<int:id>', views.addViewPostView, name="increase_view_post"),
    path('posts/<int:id>/comments', views.getCommentOfPostView, name='get_comment_post'),
    # path('comments')
    # path('comments'/<int:id>),
    # path('categories'),
]
