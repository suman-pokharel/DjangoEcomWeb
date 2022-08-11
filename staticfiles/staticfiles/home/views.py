from cProfile import label
from email.message import Message
from itertools import count
from pickle import NONE
from urllib import request
from django import views
from django.forms import SlugField
from django.shortcuts import redirect, render
from django.views import View
from .models import *
from django.views.generic import View
import datetime,random
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required




class Base(View):
	views = {}
	views['categories'] = Category.objects.all()
	views['brands'] = Brand.objects.all()
	all_brand = []
	for i in Brand.objects.all():
		ids = Brand.objects.get(name = i).id
		
		count = Product.objects.filter(brand =ids).count()
		
		all_brand.append({'product_count':count,'ids' : ids})
		
	views['counts'] = all_brand
	


class HomeView(Base):
	def get(self,request):
		self.views
		self.views['sliders'] = Slider.objects.all()
		self.views['ads'] = Ad.objects.all()
		self.views['hots'] = Product.objects.filter(labels = 'hot')
		self.views['sale'] = Product.objects.filter(labels = 'sale')
		self.views['news'] = Product.objects.filter(labels = 'new')
		l=Cart.objects.filter(username=request.user.username,checkout=False).count()
		qty=0
		for i in range(l):
			data1=Cart.objects.filter(username=request.user.username,checkout=False)[i].quantity
			qty += data1
		self.views['cart_qty']=qty
		return render(request,'index.html',self.views)


class ProductDetailView(Base):
	def get(self,request,slug):
		self.views
		self.views['details'] = Product.objects.filter(slug = slug)
		self.views['reviews'] = Review.objects.filter(slug = slug)
		names=Product.objects.get(slug=slug).name
		self.views['related_products']=Product.objects.filter(name=names)
		subcat = Product.objects.get(slug = slug).subcategory
		self.views['subcat_products'] = Product.objects.filter(subcategory = subcat)
		l=Cart.objects.filter(username=request.user.username,checkout=False).count()
		qty=0
		for i in range(l):
			data1=Cart.objects.filter(username=request.user.username,checkout=False)[i].quantity
			qty += data1
		self.views['cart_qty']=qty
		
		return render(request,'product-detail.html',self.views)

def review(request):
	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		review = request.POST['review']
		slug = request.POST['slug']
		x = datetime.datetime.now()
		date = x.strftime("%c")
		data = Review.objects.create(
			name = name,
			email = email,
			review =review,
			date = date,
			slug = slug
			)
		data.save()

	return redirect(f'/details/{slug}')


class CategoryView(Base):
	def get(self,request,slug):
		self.views
		cat_id = Category.objects.get(slug = slug).id
		self.views['cat_product'] = Product.objects.filter(category_id = cat_id)
		l=Cart.objects.filter(username=request.user.username,checkout=False).count()
		qty=0
		for i in range(l):
			data1=Cart.objects.filter(username=request.user.username,checkout=False)[i].quantity
			qty += data1
		self.views['cart_qty']=qty
		

		return render(request,'product-list.html',self.views)

class SearchView(Base):
	def get(self,request):
		self.views
		if request.method == 'GET':
			query = request.GET['query']
			self.views['search_product'] = Product.objects.filter(name__icontains = query)
			self.views['search_for'] = query
		l=Cart.objects.filter(username=request.user.username,checkout=False).count()
		qty=0
		for i in range(l):
			data1=Cart.objects.filter(username=request.user.username,checkout=False)[i].quantity
			qty += data1
		self.views['cart_qty']=qty
		return render(request,'search.html',self.views)




def signup(request):
	if request.method == 'POST':
		f_name=request.POST['first_name']
		l_name=request.POST['last_name']
		username = request.POST['username']
		email = request.POST['email']
		Password = request.POST['password']
		cpassword = request.POST['cpassword']
		if Password  == cpassword:
			if User.objects.filter(username=username).exists():
				messages.error(request,'The username is already taken')
				return redirect('/signup')
			elif User.objects.filter(email=email).exists():
				messages.error(request,'The email is already taken')
				return redirect('/signup')
			else:
				data= User.objects.create_user(
					username=username,
					email=email,
					password=Password,
					first_name=f_name,
					last_name=l_name,
				)
				data.save()
				return redirect('/')
		else:
			messages.error(request,'the password is not correct')
			return redirect('/signup')
	return render(request,'signup.html')

def contact(request):
	views={}

	if request.method == 'POST':
			Full_name = request.POST['Name']
			Email = request.POST['email']
			Subject = request.POST['subject']
			Messages= request.POST['message']
			data=Contact.objects.create(
				Name=Full_name,
				email=Email,
				subject=Subject,
				message=Messages,
			)
			data.save()
	l=Cart.objects.filter(username=request.user.username,checkout=False).count()
	qty=0
	for i in range(l):
		data1=Cart.objects.filter(username=request.user.username,checkout=False)[i].quantity
		qty += data1
	
	views['cart_qty']=qty
	return render(request,'contact.html',views)
		
	

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user= auth.authenticate(username= username, password= password)
		if user is not None:
			auth.login(request,user)
			return redirect('/')
		else:
			messages.error(request, 'The username and password does not match')
			return redirect('/login')
	return render(request,'login.html')

def logout(request):
	auth.logout(request)
	return redirect('/')


def cal(slug):
	price = Product.objects.get(slug = slug).price
	discount = Product.objects.get(slug = slug).discount
	if discount > 0 :
		actual_price = discount
	else:
		actual_price = price
	try:
		quantity = Cart.objects.get(slug = slug).quantity
	except:
		return actual_price


	return quantity,actual_price


@login_required(login_url='/login')
def add_to_cart(request,slug):
	username = request.user.username
	
	if Cart.objects.filter(slug = slug,username = username,checkout = False).exists():
		quantity,actual_price = cal(slug)
		quantity = quantity + 1
		total = actual_price * quantity

		Cart.objects.filter(slug = slug,username = username,checkout = False).update(
			quantity = quantity,
			total = total
			)
	else:
		actual_price= cal(slug)
		data = Cart.objects.create(
			username = username,
			slug = slug,
			total= actual_price,
			items = Product.objects.filter(slug = slug)[0]
			)
		data.save()
	return redirect('/my_cart')


def delete_cart(request,slug):
	username=request.user.username
	Cart.objects.filter(slug = slug,username = username,checkout = False).delete()
	return redirect('/my_cart')

def remove_cart(request,slug):
	username=request.user.username
	if Cart.objects.filter(username=username,slug=slug,checkout=False).exists():
		quantity,actual_price=cal(slug)
		if quantity > 1 :
			quantity=quantity-1
			total=quantity*actual_price

			Cart.objects.filter(slug = slug,username = username,checkout = False).update(
				quantity = quantity,
			    total = total
			)
	return redirect('/my_cart')


		
class CartView(Base):
	def get(self,request):
		self.views['my_carts']= Cart.objects.filter(username=request.user.username,checkout=False)
		grand_total= 0
		qty=0
		shipping_cost=100
		l=Cart.objects.filter(username=request.user.username,checkout=False).count()
		qty=0
		for i in range(l):
			data1=Cart.objects.filter(username=request.user.username,checkout=False)[i].quantity
			qty += data1
		self.views['cart_qty']=qty
		
		for i in range(l):
			data=Cart.objects.filter(username=request.user.username,checkout=False)[i].total
			grand_total += data
			shipping_cost=100
		grand_totalss=grand_total + shipping_cost	
		self.views['gd']=grand_totalss
		self.views['grand_totals']=grand_total
		
		return render(request,'cart.html',self.views)

class WishlistView(Base):
	def get(self,request):
		self.views['my_wishlists']=Wishlist.objects.filter(username=request.user.username,checkout=False)
		return render(request,'wishlist.html',self.views)

def delete_wishlist(request,slug):
	username=request.user.username
	Wishlist.objects.filter(slug = slug,username = username,checkout = False).delete()
	return redirect('/my_wishlist')

def remove_wishlist(request,slug):
	username=request.user.username
	if Wishlist.objects.filter(username=username,slug=slug,checkout=False).exists():
		quantity = Wishlist.objects.get(slug=slug).quantity
		if quantity > 1 :
			quantity=quantity-1
			

			Wishlist.objects.filter(slug = slug,username = username,checkout = False).update(
				quantity = quantity,
			    
			)
	return redirect('/my_wishlist')

def add_to_wishlist(request,slug):
	username = request.user.username
	if Wishlist.objects.filter(slug = slug,username = username,checkout = False).exists():
		quantity = Wishlist.objects.get(slug=slug).quantity
		quantity = quantity+1

		Wishlist.objects.filter(slug = slug,username = username,checkout = False).update(
			quantity = quantity,
			
			
			)
	else:
		
		data = Wishlist.objects.create(
			username = username,
			slug = slug,
			items = Product.objects.filter(slug = slug)[0]
			)
		data.save()
	return redirect('/my_wishlist')

		

class CheckoutView(Base):
	def get(self,request):
		self.views['my_checkout']= Cart.objects.filter(username=request.user.username,checkout=False)
		grand_total= 0
		shipping_cost=100
		l=Cart.objects.filter(username=request.user.username,checkout=False).count()
		qty=0
		for i in range(l):
			data1=Cart.objects.filter(username=request.user.username,checkout=False)[i].quantity
			qty += data1
		self.views['cart_qty']=qty
		for i in range(l):
			data=Cart.objects.filter(username=request.user.username,checkout=False)[i].total
			grand_total += data
			shipping_cost=100
		grand_totalss=grand_total + shipping_cost	
		self.views['gd']=grand_totalss
		self.views['grand_totals']=grand_total
		return render(request,'checkout.html',self.views)


def placeorder(request):
	if request.method == 'POST':
		orderplace=OrderPlace()
		orderplace.username=request.user
		orderplace.fname=request.POST.get('fname')
		orderplace.lname=request.POST.get('lname')
		orderplace.email=request.POST.get('email')
		orderplace.mobile=request.POST.get('mobile')
		orderplace.address=request.POST.get('address')
		orderplace.country=request.POST.get('country')
		orderplace.city=request.POST.get('city')
		orderplace.zipcode=request.POST.get('zipcode')
		orderplace.state=request.POST.get('state')
		orderplace.payment_mode=request.POST.get('payment_mode')
		grand_total= 0
		shipping_cost=100
		l=Cart.objects.filter(username=request.user.username,checkout=False).count()
		qty=0
		for i in range(l):
			data1=Cart.objects.filter(username=request.user.username,checkout=False)[i].quantity
			qty += data1
		for i in range(l):
			data=Cart.objects.filter(username=request.user.username,checkout=False)[i].total
			grand_total += data
			shipping_cost=100
		grand_totalss=grand_total + shipping_cost	
		orderplace.grand_totalss=grand_totalss

		tracknum='Estore'+str(random.randint(1111,9999))
		while OrderPlace.objects.filter(tracking_id=tracknum) is None:
			tracknum='Estore'+str(random.randint(1111,9999))
		orderplace.tracking_id=tracknum
		orderplace.save()

		neworderitem=Cart.objects.filter(username=request.user.username,checkout=False)
		
		for item in neworderitem:
			if item.items.discount > 0:
				actual_price=item.items.discount
			else:
				actual_price=item.items.price
			OderItems.objects.create(
				order=orderplace,
				product=item.items,
				price=actual_price,
				quantity=item.quantity,

			)
			Cart.objects.filter(username=request.user.username,checkout=False).delete()	
	return redirect('/')


	










# aayush@deepminds.xyz
# 9840059376