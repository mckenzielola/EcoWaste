from django.db import models
# to link atrributes to user
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from datetime import datetime, timedelta

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
    
""" A class to store and retrieve food carbon footprints from a predefined database.
    The food items and their carbon footprints are stored as a dictionary.
"""        
class FoodDatabase:
    # Carbon dioxide emissions associated with the production of food per lbs   
    food_CarbonFootPrint = { 
        "Beef": 60.0,
        "Lamb": 39.0,
        "Chicken": 6.9,
        "Pork": 12.0,
        "Turkey": 10.0,
        "Fish": 5.0,
        "Shrimp": 12.0,
        "Crab": 3.3,
        "Oyster": 0.9,
        "Lobster": 5.0,
        "Clams": 1.5,
        "Eggs": 4.8,
        "Milk": 1.9,
        "Yogurt": 3.3,
        "Butter": 24.0,
        "Cheddar Cheese": 21.5,
        "Mozzarella Cheese": 18.6,
        "Swiss Cheese": 18.0,
        "Parmesan Cheese": 24.0,
        "Cream Cheese": 12.0,
        "Brie Cheese": 18.5,
        "Gouda Cheese": 18.5,
        "Apple": 0.9,
        "Banana": 0.9,
        "Grapes": 0.5,
        "Pineapple": 1.3,
        "Orange": 0.6,
        "Lemon": 0.5,
        "Pear": 0.9,
        "Peach": 0.9,
        "Strawberry": 1.1,
        "Blueberry": 1.2,
        "Cherry": 1.2,
        "Raspberry": 1.2,
        "Watermelon": 0.3,
        "Melon": 0.3,
        "Kiwi": 0.9,
        "Mango": 0.8,
        "Papaya": 0.8,
        "Fig": 1.4,
        "Plum": 0.8,
        "Pomegranate": 0.7,
        "Date": 0.7,
        "Olives": 4.3,
        "Avocado": 1.8,
        "Berry": 1.2,
        "Cherries": 1.2,
        "Grapefruit": 1.1,
        "Nectarines": 0.9,
        "Cabbage": 0.3,
        "Spinach": 0.8,
        "Kale": 0.9,
        "Lettuce": 0.8,
        "Broccoli": 0.6,
        "Carrot": 0.6,
        "Zucchini": 0.5,
        "Asparagus": 1.8,
        "Cauliflower": 0.5,
        "Bell Pepper": 1.8,
        "Cucumber": 0.7,
        "Pumpkin": 0.6,
        "Tomato": 0.9,
        "Peas": 0.6,
        "Squash": 0.6,
        "Celery": 0.5,
        "Mushrooms": 0.9,
        "Onions": 0.3,
        "Peppers": 0.9,
        "Garlic": 0.6,
        "Chili": 1.5,
        "Herbs": 0.6,
        "Coriander": 0.5,
        "Rice": 4.5,
        "Wheat": 2.6,
        "Barley": 2.2,
        "Oats": 2.4,
        "Corn": 1.8,
        "Couscous": 2.5,
        "Polenta": 2.5,
        "Rye": 2.4,
        "Brown Rice": 4.1,
        "White Rice": 4.5,
        "Tortillas": 2.1,
        "Noodles": 2.5,
        "Granola": 2.5,
        "Oatmeal": 2.3,
        "Crackers": 2.5,
        "Popcorn": 1.8,
        "Cereal": 2.2,
        "Pasta": 2.0,
        "Black Beans": 0.9,
        "Kidney Beans": 0.9,
        "Soybeans": 2.0,
        "Chickpeas": 1.3,
        "Lentils": 0.9,
        "Peanuts": 0.9,
        "Almonds": 4.0,
        "Cashews": 3.9,
        "Pistachios": 4.0,
        "Walnuts": 4.0,
        "Hazelnuts": 3.6,
        "Sunflower Seeds": 1.2,
        "Chia Seeds": 2.0,
        "Flax Seeds": 1.8,
        "Olive Oil": 8.0,
        "Coconut Oil": 6.0,
        "Butter": 24.0,
        "Ghee": 12.0,
        "Margarine": 6.0,
        "Bread": 1.6,
        "Cakes": 3.3,
        "Pastries": 2.7,
        "Cookies": 2.5,
        "Pies": 2.5,
        "Muffins": 2.6,
        "Donuts": 2.7,
        "Gelato": 6.0,
        "Pudding": 1.8,
        "Brownie": 2.5,
        "Cake": 3.3,
        "Donuts": 2.7,
        "Pie": 2.5,
        "Chips": 1.8,
        "Fruit Juice": 0.9,
        "Frozen Meals": 3.5,
        "Canned Goods": 1.1,
        "Snacks": 1.2,
        "Salami": 12.0,
        "Bologna": 12.0,
        "Sausage": 12.0,
        "Bacon": 8.0,
        "Milk": 1.9,
        "Juice": 0.9,
        "Coffee": 8.0,
        "Tea": 2.5,
        "Soda": 0.9,
        "Smoothies": 1.1,
        "Energy drink": 1.5,
        "Beer": 1.8,
        "Wine": 1.8,
        "Vodka": 5.0,
        "Whiskey": 5.0,
        "Rum": 4.5,
        "Tequila": 5.0,
        "Champagne": 6.0
    }      
    
    """
    Retrieve the carbon footprint of a food item in gCO2e per kg.
    If the food item doesn't exist, return None.
    """
    @classmethod
    def get_carbon_footprint(cls, food_name):
        return cls.food_data.get(food_name)


"""
A class to calculate the environmental impact for a user based on their food consumption and waste generation.
"""
class ImpactCalculator:
    def __init__(self, user):
        self.user = user
        self.date_range = None  # Initialize date range

    def set_date_range(self, start_date, end_date):
        """
        Set the date range for calculations.
        :param start_date: The starting date (datetime.date).
        :param end_date: The ending date (datetime.date).
        """
        self.date_range = (start_date, end_date)

    def get_food_data(self):
        """
        Fetch food consumption data for the user within the selected date range.
        :return: A list of tuples (food_name, weight_in_kg).
        """
        items = Item.objects.filter(author=self.user)
        if self.date_range:
            start_date, end_date = self.date_range
            items = items.filter(expiration__range=(start_date, end_date))
        foods = [(item.perishable, item.quantity) for item in items]
        return foods

    def get_waste_data(self):
        """
        Fetch waste data for the user within the selected date range.
        :return: A list of WasteItem objects.
        """
        items = WasteItem.objects.all()  # No author field, so fetching all
        if self.date_range:
            start_date, end_date = self.date_range
            items = items.filter(date_added__range=(start_date, end_date))
        return items

    def calculate_impact(self, item_data, waste_data=None):
        """
        Calculate the total environmental impact based on the provided item data (food and waste).
        :param item_data: A list of tuples (item_name, quantity).
        :param waste_data: A list of tuples (waste_name, quantity).
        :return: The total environmental impact (gCO2e), rounded to 3 decimal places.
        """
        total_carbon_footprint = 0
        KG_TO_POUNDS = 2.20462

        # Calculate food-related carbon footprint from the received item data
        for food, quantity_in_kg in item_data:
            footprint = FoodDatabase.get_carbon_footprint(food)
            if footprint:
                weight_in_pounds = quantity_in_kg * KG_TO_POUNDS
                total_carbon_footprint += round(footprint * weight_in_pounds, 3)

        # Calculate waste-related carbon footprint from the provided waste data
        if waste_data:
            for waste_name, waste_quantity in waste_data:
                footprint = FoodDatabase.get_carbon_footprint(waste_name)
                if footprint:
                    total_carbon_footprint += round(footprint * waste_quantity, 3)

        # Waste impact: Adding extra impact for each waste item
        total_impact = total_carbon_footprint + (len(waste_data) * 2) if waste_data else total_carbon_footprint
        return round(total_impact, 3)

    def get_co2footprint_report(self):
        impact = self.calculate_impact()
        return f"{impact}"  # Just return the CO2 impact value without extra text

    def get_waste_report(self):
        total_waste = sum(item.quantity for item in self.get_waste_data())
        if self.date_range:
            start_date, end_date = self.date_range
            date_info = f"from {start_date} to {end_date}"
        else:
            date_info = "for all time"
        return f"Total waste for {self.user.username} ({date_info}): {total_waste} lbs"
