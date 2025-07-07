from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Diary(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    diary_entry = models.ForeignKey(Diary, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    diary_entry = models.ForeignKey(Diary, on_delete = models.CASCADE, null = True, blank = True)
    comment_entry = models.ForeignKey(Comment, on_delete = models.CASCADE, null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    is_like = models.BooleanField(default = False)


