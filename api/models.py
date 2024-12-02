from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
            return f'{self.first_name} - {self.last_name}'


class Post(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    view_count = models.IntegerField(default=0)
    publish_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.SET('Deleted Account'))
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    published_date = models.DateTimeField()

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
    