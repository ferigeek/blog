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
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('v1/posts', views.PostsView.as_view(), name='posts'),
    path('v1/posts/<int:id>', views.PostView.as_view(), name="post"),
    path('v1/posts/<int:id>/comments', views.PostCommentView.as_view(), name='get_comment_post'),
    path('v1/comments', views.CommentsView.as_view(), name='comments'),
    path('v1/comments/<int:id>', views.CommentView.as_view(), name='comment'),
    path('v1/categories', views.CategoriesView.as_view(), name='categories'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)