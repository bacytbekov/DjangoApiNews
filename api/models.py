from django.db import models


class Workers(models.Model):
    name = models.CharField(max_length=100)
    login =models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=100)
    subTitle = models.CharField(max_length=100,null=True,blank=True)
    content = models.TextField(max_length=1000)
    dateTime = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    image_url = models.CharField(max_length=500, null=True, blank=True)
# Create your models here.
