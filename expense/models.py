from django.db import models
from django.urls import reverse
from django.conf import settings
# Create your models here.
class Customer(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

class Income(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type

class Expenditure(models.Model):
    category = models.CharField(max_length=100)
    budget = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.category
    
class Data(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, default=1)
    sub_category = models.CharField(max_length=100)
    sub_category_link=models.ForeignKey(Expenditure,on_delete=models.CASCADE)
    spent = models.IntegerField()
    balance = models.IntegerField(blank=True,null=True)
    recursive= models.BooleanField(max_length=100) 
    pay_type = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)   
    
    def __str__(self):
        return self.sub_category
    
#    def get_absolute_url(self):
#        return reverse("expense:post_detail",kwargs={"id": self.id})
    class Meta:
        ordering = ["-timestamp","-updated"]