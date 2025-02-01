from django.contrib import admin
# Register your models here.
from apps.product.models import Category,ProductDescription,Attribute,AttributeOption, Payment, Product, Order, OrderProduct

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    search_fields = ['name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user','total_price')
    search_fields = ['user__email']

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('id','quantity','price')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id','status']

@admin.register(ProductDescription)
class ProductDescriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'label']

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    
@admin.register(AttributeOption)
class AttributeOptionAdmin(admin.ModelAdmin):
    list_display = ['id','option']