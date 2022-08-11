from django.urls import path
from .views import*
urlpatterns = [
    
    path('',HomeView.as_view(),name='home'),
    path('details/<slug>',ProductDetailView.as_view(),name='details'),
    path('add_review', review, name='add_review'),
	path('category/<slug>', CategoryView.as_view(), name='category'),
	path('search', SearchView.as_view(), name='search'),
    path('signup',signup,name='signup'),
    path('contact',contact,name='contact'),
    path('login',login,name='login'),
    path('logout',logout,name='logout'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('delete-cart/<slug>',delete_cart,name='delete-cart'),
    path('remove-cart/<slug>',remove_cart,name='remove-cart'),
    path('my_cart/', CartView.as_view(), name='my_cart'),
    path('my_wishlist/', WishlistView.as_view(), name='my_wishlist'),
    path('delete-wishlist/<slug>',delete_wishlist,name='delete-wishlist'),
    path('add-to-wishlist/<slug>', add_to_wishlist, name='add-to-wishlist'),
    path('remove-wishlist/<slug>',remove_wishlist,name='remove-wishlist'),
    path('checkout/',CheckoutView.as_view(),name='checkout'),
    path('placeorder/',placeorder,name='placeorder'),
   

]


