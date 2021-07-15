from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model
from django.utils.translation import TranslatorCommentWarning

class User(AbstractUser):
    pass

class listing(models.Model):
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    title  = models.CharField("title",max_length=14,default="not provided")
    description = models.CharField("description",max_length=200,blank=True)
    price = models.IntegerField("price",default=0)
    image = models.URLField(max_length=256,default="not provided", null=True)
    watchlist_user = models.ManyToManyField(User ,blank=True,related_name="watchlist_user")
    category = models.CharField(max_length=74,blank=True) 
    closed = models.BooleanField(default=False)
    winner = models.CharField(max_length=70,blank=True)

    def __str__(self):
       return f"{self.title}"

class watchlist(models.Model):
    user = models.CharField(max_length=80)
    list_id = models.IntegerField()
     
class Bid(models.Model):
    user = models.CharField(max_length=70)
    title = models.CharField(max_length=70)
    list_id = models.IntegerField()
    bid = models.IntegerField()

class Comment(models.Model):
    user = models.CharField(max_length=70)
    comment = models.CharField(max_length=90)
    list_id = models.IntegerField()