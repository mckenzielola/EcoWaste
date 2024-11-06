from django import forms
from .models import WasteItem

class WasteItemForm(forms.ModelForm):
    class Meta:
        model = WasteItem
        fields = ('name', 'category', 'quantity')