from graphene_django.types import DjangoObjectType
import graphene

from ..models import *

class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = '__all__'

class PostType(DjangoObjectType):
    class Meta:
        model = Post