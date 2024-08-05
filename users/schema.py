import graphene

from .models import *
from graphene_django.types import DjangoObjectType
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from .serializers import *
from .mutations.Usermutations import UserMutationHub
from .shared.types import *


class Query(graphene.ObjectType):
    all_CustomUser = graphene.List(UserType, id=graphene.Int())
    all_Category = graphene.List(CategoryType, id=graphene.Int())
    all_Post = graphene.List(PostType)

    def resolve_all_Category(self, info, id=None):
        query = Category.objects.all()
        if id:
            query = Category.objects.filter(id=id)
        return query

    def resolve_all_CustomUser(self, info, id=None):
        query = CustomUser.objects.filter(is_superuser=False)
        if id:
            query = CustomUser.objects.filter(is_superuser=False, id=id)
        return query

    def resolve_all_Post(self, info, **kwargs):
        return Post.objects.all()


#     def resolve_list_of_category_content(self, info, categorydata ):
#         categories = Category.objects.all()
#         if categorydata:
#             categories = Category.objects.filter(name=categorydata).order_by('-id')[:4]

#         listOfmainPageContent = []
#         for category in categories:
#             pageData = Post.objects.filter(category=category)
#             spliterByCategory = MainPageType(
#                 category = category,
#                 post_list = pageData
#             )
#             listOfmainPageContent.append(spliterByCategory)
#         return (ListOfCategoryContent(ListOfPost=listOfmainPageContent))


class Mutation(UserMutationHub, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
