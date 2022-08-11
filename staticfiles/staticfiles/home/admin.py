from django.contrib import admin
from .models import *


class OrderItemsTubleinline(admin.TabularInline):
    model = OderItems

class OrderPlaceAdmin(admin.ModelAdmin):
    inlines = [OrderItemsTubleinline]


# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Slider)
admin.site.register(Ad)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Review)
admin.site.register(Contact)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(OrderPlace,OrderPlaceAdmin)
admin.site.register(OderItems)