import graphene
from apps.base.utils import get_object_or_none, generate_message, create_graphql_error
from .objectType import CategoryType, ProductType, OrderProductType, OrderType
from apps.base.utils import get_object_by_kwargs
from backend.authentication import isAuthenticated

from datetime import datetime
from graphene_django.forms.mutation import DjangoFormMutation
from apps.product.forms import OrderProductAttributeForm, ReviewForm,FAQForm, ProductForm, CategoryForm, OrderForm, OrderProductForm, PaymentForm, CredentialForm, AttributeOptionForm, ProductDescriptionForm, AttributeForm
from apps.product.models import OrderProductAttribute,FAQ, Review, Category, Product, Order, OrderProduct,  Payment, Credential, AttributeOption, Attribute, ProductDescription
from apps.accounts.models import Address, UserRole
import json 
from django.utils.timezone import now
from datetime import timedelta
from graphql import GraphQLError
import random
import string
import uuid

class OrderProductAttributeCUD(DjangoFormMutation):
    message = graphene.String()
    success = graphene.Boolean()
    
    class Meta:
        form_class = OrderProductAttributeForm
    
    @isAuthenticated()
    def mutate_and_get_payload(self, info, **input):
            
        instance = get_object_or_none(OrderProductAttribute, id=input.get('id'))
        form = OrderProductAttributeForm(input, instance=instance)
        if not form.is_valid():
            return create_graphql_error(form)

        orderProductAttribute = form.save()

        return OrderProductAttributeCUD(
                message="Created successfully",
                success=True,
            )
        

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
            
        if form.is_valid():
            order = form.save()
            return PaymentCUD( success=True)
        create_graphql_error(form.errors)
class ReviewCUD(DjangoFormMutation):
    success = graphene.Boolean()
    class Meta:
        form_class = ReviewForm

    @isAuthenticated([UserRole.CUSTOMER, UserRole.ADMIN])
    def mutate_and_get_payload(self, info, **input):
        try:
            input['user'] = info.context.User.id
            instance = get_object_or_none(Review, id=input.get("id"))
            form = ReviewForm(input, instance=instance)
            if not form.is_valid():
                create_graphql_error(form.errors) 
                
            form.save()
            return ReviewCUD(success=True) 
        except Exception as e:
            return GraphQLError("Server error!")



class DeleteReview(graphene.Mutation):
    message = graphene.String()
    success = graphene.Boolean()    
    class Arguments:
        id = graphene.ID(required=True)
    def mutate(self, info, id):
        review = get_object_by_kwargs(Review, {"id": id})
        review.delete()
        return DeleteReview(success=True, message="Deleted!")
class FAQCUD(DjangoFormMutation):
    success = graphene.Boolean()
    class Meta:
        form_class = FAQForm
    
    def mutate_and_get_payload(self, info, **input):
        instance = get_object_or_none(FAQ, id=input.get("id"))
        form = FAQForm(input, instance=instance)
        if not form.is_valid():
            create_graphql_error(form.errors) 
            
        form.save()
        return FAQCUD(success=True ) 

class Mutation(graphene.ObjectType):
    review_cud = ReviewCUD.Field()
    delete_review = DeleteReview.Field()
    faq_cud = FAQCUD.Field()

    product_cud = ProductCUD.Field()
    delete_product = DeleteProduct.Field()
    category_cud = CategoryCUD.Field()
    order_cud = OrderCUD.Field()
    order_product_cud = OrderProductCUD.Field()
    payment_cud = PaymentCUD.Field()
    order_product_attribute_cud = OrderProductAttributeCUD.Field()
    
    
    