from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    data = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner", null=True)

    def get_likes(self):
        likes = 0
        try:
            likes = Likes.objects.filter(liketo=self.id)
            return likes
        except Likes.DoesNotExist:
            return likes

    def __str__(self):
        return f"ID: {self.id};Owner: {self.owner}; Data: {self.data}; Date: {self.date}"


class Followers(models.Model):
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following")
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower")

    def __str__(self):
        return f"THE FOLLOWER: {self.follower}; TO FOLLOWING: {self.following};"


class Likes(models.Model):
    liker = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="liker")
    liketo = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="liketo")

    def __str__(self):
        return f"LIKED BY: {self.liker}; THE POST: {self.liketo};"
