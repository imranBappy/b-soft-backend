import graphene
from apps.product.models import FAQ, Review, Product, Category,Coupon, Order,Credential, ProductDescription,Attribute,AttributeOption, OrderProduct, Address,  Payment
from apps.accounts.models import Address
from apps.base.utils import get_object_by_kwargs
from apps.product.objectType import ReviewType, FAQType, CredentialType, AttributeOptionType, AttributeType, ProductDescriptionType, CouponType, CategoryType, ProductType, SubCategoryType, PaymentType, OrderType, OrderProductType
from graphene_django.filter import DjangoFilterConnectionField


class Query(graphene.ObjectType):
    faq = graphene.Field(FAQType, id=graphene.ID(required=True))
    faqs = DjangoFilterConnectionField(FAQType)

    review = graphene.Field(ReviewType, id=graphene.ID(required=True))
    reviews = DjangoFilterConnectionField(ReviewType)

    credential = graphene.Field(CredentialType, id=graphene.ID(required=True))
    credentials = DjangoFilterConnectionField(CredentialType)
    
    attribute_option = graphene.Field(AttributeOptionType, id=graphene.ID(required=True))
    attribute_option = DjangoFilterConnectionField(AttributeOptionType)
    
    attribute = graphene.Field(AttributeType, id=graphene.ID(required=True))
    attributes = DjangoFilterConnectionField(AttributeType)
    
    product_description = graphene.Field(ProductDescriptionType, id=graphene.ID(required=True))
    product_descriptions = DjangoFilterConnectionField(ProductDescriptionType)
    
    coupon = graphene.Field(CouponType, id=graphene.ID(required=True))
    coupons = DjangoFilterConnectionField(CouponType)
    
    category = graphene.Field(CategoryType, id=graphene.ID(required=True))
    categories = DjangoFilterConnectionField(CategoryType)
    
    subcategory = graphene.Field(CategoryType, id=graphene.ID(required=True))
    subcategories = DjangoFilterConnectionField(SubCategoryType, parent_id=graphene.ID(required=True))
    
    product = graphene.Field(ProductType, id=graphene.ID(required=True))
    products = DjangoFilterConnectionField(ProductType)
    
    order = graphene.Field(OrderType, id=graphene.ID(required=True))
    orders = DjangoFilterConnectionField(OrderType)
    
    order_product = graphene.Field(OrderProductType, id=graphene.ID(required=True))
    order_products = DjangoFilterConnectionField(OrderProductType)
    

    payment = graphene.Field(PaymentType, id=graphene.ID(required=False), order=graphene.ID(required=False))
    payments = DjangoFilterConnectionField(PaymentType)
    
    def resolve_review(self, info, id):
        return get_object_by_kwargs(Review, {"id": id})
     
    def resolve_reviews(self, info, **kwargs):
        return Review.objects.all()

    def resolve_faq(self, info, id):
        return get_object_by_kwargs(FAQ, {"id": id})
     
    def resolve_faqs(self, info, **kwargs):
        return FAQ.objects.all()

    def resolve_category(self, info, id):
        return get_object_by_kwargs(Category, {"id": id})
     
    def resolve_categories(self, info ,**kwargs):
        return Category.objects.order_by("-created_at")

    def resolve_subcategory(self, info, id):
        return get_object_by_kwargs(Category, {"id": id})
     
    def resolve_subcategories(self, info, **kwargs):
        return Category.objects.filter(parent=kwargs.get("parent_id"))
        

    def resolve_product(self, info, id):
        return get_object_by_kwargs(Product, {"id": id})
     
    def resolve_products(self, info, **kwargs):
        return Product.objects.all()
    
    def resolve_order(self, info, id):
        return get_object_by_kwargs(Order, {"id": id})
     
    def resolve_orders(self, info, **kwargs):
        return Order.objects.all()  
    
    def resolve_order_product(self, info, id):
        return get_object_by_kwargs(OrderProduct, {"id": id})
     
    def resolve_order_products(self, info, **kwargs):
        return OrderProduct.objects.all()
    
    def resolve_payment(self, info, id, order=None):
        if order:
            result =  get_object_by_kwargs(Payment, { 'order': order})
            return result
        return get_object_by_kwargs(Payment, {'id': id})
     
    def resolve_payments(self, info, **kwargs):
        return Payment.objects.all()
    
    
    
    def elastic_search(self, info, **kwargs):
        pass
    
