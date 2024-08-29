from django.db import models
from django.utils.timezone import datetime

class Users(models.Model):
    name = models.CharField(max_length=100, null=True)

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return self.name
class Notes(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
