import graphene
from ..serializers import *
from ..shared.types import *
import graphql_jwt
from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import get_token 
from graphql_jwt.utils import jwt_payload, jwt_encode

class CreateUserMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        phone_number = graphene.String(required=True)
        password = graphene.String(required=True)


    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, username, email, password):
        success = True
        errors = []
       
        # Create user
        if email and CustomUser.objects.filter(email=email).exists():
            errors = ["Email must be unique."]
        try: 
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
        except Exception as e:
            errors.append(e)
        # Generate token
        # token = graphql_jwt.utils.jwt_encode(user).decode('utf-8')
        return CreateUserMutation(success=success, errors=errors)

class CategoryCreateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)
        created_by = graphene.Int(required=True)
        modifie_by = graphene.Int()

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    category_type = graphene.Field(CategoryType)

    def mutate(self, info, **kwargs):
        success = False
        errors = []
        category_instance = None
        
        if 'id' in kwargs and kwargs['id']:
            # Update operation
            category_instance = Category.objects.filter(id=kwargs['id']).first()
            if not category_instance:
                errors.append("Category not found.")
            else:
                serializer = CategorySerializer(category_instance, data=kwargs, partial=True)
        else:
            # Create operation
            serializer = CategorySerializer(data=kwargs)

        if serializer.is_valid():
            try:

                serializer.save()
                category_instance = serializer.instance
                success = True
            except Exception as e:
                errors.append(str(e))
        else:
            errors = [f"{field}: {'; '.join([str(e) for e in error])}" for field, error in serializer.errors.items()]



#         return CategoryCreateMutation(success=success, errors=errors, category_type=category_instance)

class PostCreateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String(required=True)
        image = graphene.String()
        content = graphene.String()
        category = graphene.Int()
        date = graphene.String()
        active = graphene.Boolean()
        created_by = graphene.Int(required=True)
        modifie_by = graphene.Int()

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    # post_type = graphene.Field(PostType)

    def mutate(self, info, **kwargs):
        success = False
        errors = []
        # post_instance = None 
        if 'id' in kwargs and kwargs['id']:
            # Update operation
            post_instance = Post.objects.filter(id=kwargs['id']).first()
            if not post_instance:
                errors.append("Post not found.")
            else:
                serializer = PostSerializer(post_instance, data=kwargs, partial=True)
        else:
            # Create operation
            serializer = PostSerializer(data=kwargs)

        if serializer.is_valid():
            try:
                serializer.save()
                post_instance = serializer.instance
                success = True
            except Exception as e:
                errors.append(str(e))
        else:
            errors = [f"{field}: {'; '.join([str(e) for e in error])}" for field, error in serializer.errors.items()]

        return PostCreateMutation(success=success, errors=errors)

class ObtainJSONWebTokenWithEmail(graphene.Mutation):
    token = graphene.String()
    user = graphene.Field(UserType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, email, password):
        user_model = get_user_model()  # Get the user model class
        user = None
        success = False
        errors = []

        try:
            user = user_model.objects.get(email=email)
            if not user.check_password(password):
                errors.append('Invalid credentials')
            else:
                # Generate JWT token if credentials are valid
                payload = jwt_payload(user)
                token = jwt_encode(payload)
                return cls(token=token, user=user, success=True, errors=errors)
        except user_model.DoesNotExist:
            errors.append('Invalid credentials')

        return cls(token=None, user=None, success=success, errors=errors)


class UserMutationHub(graphene.ObjectType):
    rigister = CreateUserMutation.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    # post_create_mutation = PostCreateMutation.Field()
    login_mutation = ObtainJSONWebTokenWithEmail.Field()
    category_create_mutation = CategoryCreateMutation.Field()


