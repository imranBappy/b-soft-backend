import graphene
from apps.base.utils import get_object_or_none, generate_message, create_graphql_error
from .objectType import CategoryType, ProductType, OrderProductType, OrderType
from apps.base.utils import get_object_by_kwargs
from backend.authentication import isAuthenticated

from datetime import datetime
from graphene_django.forms.mutation import DjangoFormMutation
from apps.product.forms import ProductForm, CategoryForm, OrderForm, OrderProductForm, PaymentForm, CredentialForm, AttributeOptionForm, ProductDescriptionForm, AttributeForm
from apps.product.models import Category, Product, Order, OrderProduct,  Payment, Credential, AttributeOption, Attribute, ProductDescription
from apps.accounts.models import Address
import json 
from django.utils.timezone import now
from datetime import timedelta
from graphql import GraphQLError
import random
import string
import uuid

class CategoryCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    category = graphene.Field(CategoryType)
    
    class Meta:
        form_class = CategoryForm
    
    # @isAuthenticated(['Manager', 'Admin'])
    def mutate_and_get_payload(self, info, **input):
            
        instance = get_object_or_none(Category, id=input.get('id'))
        form = CategoryForm(input, instance=instance)
        if form.is_valid():
            category = form.save()
            return CategoryCUD(
                message="Created successfully",
                success=True,
                category=category
            )
        


class ProductDescriptionCUD(DjangoFormMutation):
    success = graphene.Boolean()

    class Meta:
        form_class = AttributeForm

    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(ProductDescription, id=input.get("id"))
        form = AttributeOptionForm(input, instance=instance)
        if not form.is_valid():
            create_graphql_error(form.errors) 
            
        form.save()
        return ProductDescriptionCUD(  success=True )  

class AttributeCUD(DjangoFormMutation):
    success = graphene.Boolean()

    class Meta:
        form_class = AttributeForm

    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(Attribute, id=input.get("id"))
        form = AttributeOptionForm(input, instance=instance)
        if not form.is_valid():
            create_graphql_error(form.errors) 
            
        form.save()
        return AttributeCUD(  success=True )  
class AttributeOptionCUD(DjangoFormMutation):
    success = graphene.Boolean()

    class Meta:
        form_class = AttributeOptionForm

    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(AttributeOption, id=input.get("id"))
        form = AttributeOptionForm(input, instance=instance)
        if not form.is_valid():
            create_graphql_error(form.errors) 
            
        form.save()
        return AttributeOptionCUD(  success=True )  
    

class CredentialCUD(DjangoFormMutation):
    success = graphene.Boolean()

    class Meta:
        form_class = CredentialForm

    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(Credential, id=input.get("id"))
        form = CredentialForm(input, instance=instance)
        if not form.is_valid():
            create_graphql_error(form.errors) 
            
        form.save()
        return CredentialCUD(  success=True )  


class ProductCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    product = graphene.Field(ProductType)

    class Meta:
        form_class = ProductForm

    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(Product, id=input.get("id"))
        form = ProductForm(input, instance=instance)
        if not form.is_valid():
            create_graphql_error(form.errors) 
            
        product = form.save()
        return ProductCUD(
                message="Created successfully!", 
                success=True,
                product=product
            ) 
        
class DeleteProduct(graphene.Mutation):
    message = graphene.String()
    success = graphene.Boolean()    
    class Arguments:
        id = graphene.ID(required=True)
    def mutate(self, info, id):
        product = get_object_by_kwargs(Product, {"id": id})
        product.delete()
        return DeleteProduct(success=True, message="Deleted!")

class OrderCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    order = graphene.Field(OrderType)
    
    class Meta:
        form_class = OrderForm

    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(Order, id=input.get('id'))
        form = OrderForm(input, instance=instance)

        if not input.get('order_id'):
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
            order_id = f"#{random_string}"
            input['order_id'] = order_id
        
        if form.is_valid()  == False:
            return create_graphql_error(form) 
        order = form.save()
        return OrderCUD(message="Created successfully!", success=True, order=order)
    

class OrderProductCUD(DjangoFormMutation):
    success = graphene.Boolean()
    id = graphene.ID()
    class Meta:
        form_class = OrderProductForm

    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(OrderProduct, id=input.get('id'))
        form = OrderProductForm(input, instance=instance)
        if form.is_valid():
            order = form.save()
            return OrderProductCUD( success=True, id=order.id)


class PaymentCUD(DjangoFormMutation):
    success = graphene.Boolean()
    class Meta:
        form_class = PaymentForm

    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(Payment, id=input.get('id'))
        form = PaymentForm(input, instance=instance)
        # if not input.get('trx_id'):
        #     trx_id = ''.join(random.choices(string.ascii_uppercase + string.digits , k=15))
        #     input['trx_id'] =trx_id
            
        if form.is_valid():
            order = form.save()
            return PaymentCUD( success=True)
        create_graphql_error(form.errors)


class Mutation(graphene.ObjectType):
    product_cud = ProductCUD.Field()
    delete_product = DeleteProduct.Field()
    category_cud = CategoryCUD.Field()
    order_cud = OrderCUD.Field()
    order_product_cud = OrderProductCUD.Field()
    payment_cud = PaymentCUD.Field()
    
    
    
    
    