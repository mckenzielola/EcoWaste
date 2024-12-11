from django import forms
from .models import WasteItem
from .models import Item

class WasteItemForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True, label="Waste Name")
    category = forms.CharField(max_length=100, required=True, label="Category")
    quantity = forms.CharField(max_length=100, required=True, label="Quantity")

    class Meta:
        model = WasteItem
        fields = ('name', 'category', 'quantity')

    # Override the save method to set the 'name' field dynamically
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
    
# create a form for adding perishable items to freshness tracker
class PerishableItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['perishable', 'quantity', 'expiration', 'category']