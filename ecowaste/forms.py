from django import forms
from .models import WasteItem

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