from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    
    choises =[
      ('COMPUTER','computer'),
        ('HOME','home'),
        ('KIDS','kids'),
        ('FOOD','food'),
    ]
    name = models.CharField(max_length=200, default='', blank=False)
    slug = models.SlugField(unique=True, db_index= True, blank= True, null = True)
    description = models.TextField(max_length=1000,default='', blank=False)
    price = models.DecimalField(max_digits=7,decimal_places=3,default=0)
    brand = models.CharField(max_length=200, default='', blank=False)
    Catogery = models.CharField(max_length=200, choices=choises)
    rating= models.DecimalField(max_digits=3,decimal_places=2,default=0)
    stock = models.IntegerField(default=0)
    createat = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
  
class Review(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    rating = models.IntegerField(default=0)
    comment = models.TextField(max_length=1000,default='', blank=True)
    product = models.ForeignKey(Product, null=True, related_name='review', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment