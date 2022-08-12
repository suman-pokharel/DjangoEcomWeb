from datetime import date
from distutils.command.upload import upload
import email
from email import message
from email.mime import image
from itertools import product
from telnetlib import STATUS
from tkinter import CASCADE
from unicodedata import category, name
from django.db import models
from django.forms import CharField
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100)
    icon=models.CharField(max_length=200)
    slug=models.TextField(unique=True)

    def __str__(self):
        return self.name



class SubCategory(models.Model):
    name=models.CharField(max_length=100)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    icon=models.CharField(max_length=200,blank=True)
    slug=models.TextField(unique=True)

    def __str__(self):
        return self.name


STATUS=(('active','Active'),('','Default'))
class Slider(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='media')
    text=models.TextField(blank=True)
    rank=models.IntegerField()
    status=models.CharField(choices=STATUS,blank=True,max_length=100)

    def __str__(self):
        return self.name

class Ad(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='media')
    text=models.TextField(blank=True)
    rank=models.IntegerField()

    def __str__(self):
        return self.name


class Brand(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='media')
    rank=models.IntegerField()

    def __str__(self):
        return self.name

LABELS=(('new','New'),('hot','Hot'),('sale','Sale'),('','default'))
STOCK=(('In stock','In Stock'),('out of stock','Out of Stock'))
class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    discount=models.IntegerField(default=0)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory=models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE,default= 1)
    image=models.ImageField(upload_to='media')
    description=models.TextField(blank=True)
    specification=models.TextField(blank=True)
    slug=models.TextField(unique=True)
    labels=models.CharField(choices=LABELS,max_length=200)
    stock=models.CharField(choices=STOCK,max_length=200)

    def __str__(self):
        return self.name


class Review(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    review=models.TextField(blank=True)
    date=models.CharField(max_length=100)
    slug=models.TextField()
    point=models.IntegerField(default=1)
    
    def __str__(self):
        return self.name


class Contact(models.Model):
    Name=models.CharField(max_length=300)
    email=models.EmailField(max_length=200)
    subject=models.CharField(max_length=700)
    message=models.TextField()



    def __str__(self):
      return self.Name

class Cart(models.Model):
    username=models.CharField(max_length=200)
    quantity=models.IntegerField(default=1)
    checkout=models.BooleanField(default=False)
    slug=models.TextField()
    total=models.IntegerField()
    items=models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
       return self.username


class Wishlist(models.Model):
    username=models.CharField(max_length=200)
    quantity=models.IntegerField(default=1)
    checkout=models.BooleanField(default=False)
    slug=models.TextField()
    items=models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
       return self.username

class OrderPlace(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE)
    fname=models.CharField(max_length=100, null=False)
    lname=models.CharField(max_length=100, null=False)
    email=models.EmailField(max_length=100, null=False)
    mobile=models.CharField(max_length=100, null=False)
    address=models.TextField(null=False)
    country=models.CharField(max_length=100, null=False)
    city=models.CharField(max_length=100, null=False)
    zipcode=models.CharField(max_length=100, null=False)
    state=models.CharField(max_length=100, null=False)
    payment_mode=models.CharField(max_length=100, null=False)
    grand_totalss=models.IntegerField()
    payment_id=models.CharField(max_length=100, null=True)
    orderstatus=(
        ('Pending','Pending'),
        ('On the way','On the way'),
        ('completed','completed'),
    )
    status=models.CharField(max_length=100, choices=orderstatus, default='Pending')
    message=models.TextField(null=True)
    tracking_id=models.CharField(max_length=100, null=True)
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
       return '{} - {}'.format(self.id,self.tracking_id)




class OderItems(models.Model):
    order=models.ForeignKey(OrderPlace,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(null=False)
    price=models.IntegerField(default=0)
    def __str__(self):
        return '{}-{}'.format(self.order.id,self.order.tracking_id)
    

