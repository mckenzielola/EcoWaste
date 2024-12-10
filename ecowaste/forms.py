from django import forms
from .models import WasteItem

class WasteItemForm(forms.ModelForm):
    # Food options (Name of Food and their Carbon Footprint)
    FOOD_CATEGORIES = [
    ('Meat', [
        "Beef", "Lamb", "Chicken", "Pork", "Turkey"
    ]),
    ('Seafood', [
        "Fish", "Shrimp", "Crab", "Oyster", "Lobster", "Clams"
    ]),
    ('Dairy Products', [
        "Eggs", "Milk", "Yogurt", "Butter", "Cheddar Cheese", "Mozzarella Cheese", 
        "Swiss Cheese", "Parmesan Cheese", "Cream Cheese", "Brie Cheese", "Gouda Cheese"
    ]),
    ('Fruits', [
        "Apple", "Banana", "Grapes", "Pineapple", "Orange", "Lemon", 
        "Pear", "Peach", "Strawberry", "Blueberry", "Cherry", "Raspberry", 
        "Watermelon", "Melon", "Kiwi", "Mango", "Papaya", "Fig", "Plum", 
        "Pomegranate", "Date", "Olives", "Avocado", "Berry", "Cherries", 
        "Grapefruit", "Nectarines"
    ]),
    ('Vegetables and Herbs', [
        "Cabbage", "Spinach", "Kale", "Lettuce", "Broccoli", "Carrot", 
        "Zucchini", "Asparagus", "Cauliflower", "Bell Pepper", "Cucumber", 
        "Pumpkin", "Tomato", "Peas", "Squash", "Celery", "Mushrooms", "Onions", 
        "Peppers", "Garlic", "Chili", "Herbs", "Coriander"
    ]),
    ('Grains and Cereals', [
        "Rice", "Wheat", "Barley", "Oats", "Corn", "Couscous", "Polenta", 
        "Rye", "Brown Rice", "White Rice", "Tortillas", "Noodles", "Granola",
        "Oatmeal", "Crackers","Popcorn", "Cereal", "Pasta"
    ]),
    ('Legumes and Beans', [
        "Black Beans", "Kidney Beans", "Soybeans", "Chickpeas", "Lentils", 
        "Peanuts"
    ]),
    ('Nuts and Seeds', [
        "Almonds", "Cashews", "Pistachios", "Walnuts", "Hazelnuts", "Sunflower Seeds", 
        "Chia Seeds", "Flax Seeds"
    ]),
    ('Oils and Fats', [
        "Olive Oil", "Coconut Oil", "Butter", "Ghee", "Margarine"
    ]),
    ('Bakery and Confectionery', [
        "Bread", "Cakes", "Pastries", "Cookies", "Pies", "Muffins", "Donuts", 
        "Gelato", "Pudding", "Brownie", "Cake", "Donuts", "Pie"
    ]),
    ('Processed and Packaged Foods', [
        "Chips", "Fruit Juice", "Frozen Meals", "Canned Goods", "Snacks", 
        "Salami", "Bologna", "Sausage", "Bacon"
    ]),
    ('Beverages', [
        "Milk", "Juice", "Coffee", "Tea", "Soda", "Smoothies", "Energy drink"
        "Beer", "Wine", "Vodka", "Whiskey", "Rum", "Tequila", "Champagne"
    ])
    ]

    CATEGORY_CHOICES = [(category, category) for category, foods in FOOD_CATEGORIES]

    food = forms.ChoiceField(choices=[
        (food, food) for category, foods in FOOD_CATEGORIES for food in foods
    ], required=True)

    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=True)

    class Meta:
        model = WasteItem
        fields = ('food', 'category', 'quantity')

    # Override the save method to set the 'name' field dynamically
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Set the name field to the selected food name
        instance.name = self.cleaned_data['food']
        if commit:
            instance.save()
        return instance