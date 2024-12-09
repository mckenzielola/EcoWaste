from django.contrib import admin
from . import models
from .models import Article

# Register your models here.
admin.site.register(models.Item)
admin.site.register(Article)