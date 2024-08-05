from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from rest_framework.exceptions import ValidationError
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(blank=True, null=True , verbose_name="email")
    phone_number = models.CharField(blank=True, null=True, max_length=15)
    isadmin = models.BooleanField(default=False)
    isUser = models.BooleanField(default=True)
    isReporter = models.BooleanField(default=False)
    USERNAME_FIELD = "username"  # e.g: "username", "email"
    EMAIL_FIELD = "email"
 

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="categoryCreatedBy")
    modifie_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,  null=True, blank=True, related_name="categorymodifie_by")
    created_at = models.DateTimeField(auto_now_add=True)
    modifie_at = models.DateTimeField(auto_now=True)

class Post(models.Model):
    title = models.CharField(max_length=250)
    image = models.CharField(max_length=250, null=True, blank=True)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    date = models.DateField()
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="postCreatedBy")
    modifie_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="postmodifie_by")
    created_at = models.DateTimeField(auto_now_add=True)
    modifie_at = models.DateTimeField(auto_now=True)