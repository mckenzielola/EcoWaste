from django.db import models
# to link atrributes to user
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    perishable = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()

    # if user is deleted, delete all entries of db table related to the user
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    expiration = models.DateField()

class WasteItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    quantity = models.CharField(max_length=50)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category})"
    
# create dunder string method
    def __str__(self):
        return self.perishable