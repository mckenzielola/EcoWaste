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
    category = models.CharField(max_length=50, default='Other')

class WasteItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category})"
    
# create dunder string method
    def __str__(self):
        return self.perishable    
    """
    Convert CO₂e from kilograms to pounds.
    """
    def convert_kg_to_lbs(kg):
        kg_to_lbs = 2.20462
        return kg * kg_to_lbs
    
""" A class to store and retrieve food carbon footprints from a predefined database.
    The food items and their carbon footprints are stored as a dictionary.
"""        
class FoodDatabase: 
    # Carbon dioxide equivalent (CO₂e) emissions associated with the production of food per lbs  
    # Co2e unit is kg, should multiply 2.2 to convert it to lbs 
    food_CarbonFootPrint_coef = { 
        "Beef": 27.0, 
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

        "Frozen Meals": 3.5,
        "Canned Goods": 1.1,
        "Snacks": 1.2,
        "Salami": 12.0,
        "Bologna": 12.0,
        "Sausage": 12.0,
        "Bacon": 8.0,
                
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
    coefficients for biowaste generated in grams per kilogram of a specific product's waste
    These numbers help estimate the amount of biowaste that would result from the disposal 
    or production of 1 kg of a given item.
    Sources to generate the Biodegradable coef :
    https://www.sciencedirect.com/science/article/abs/pii/S0924224423004028
    https://www.fao.org/platform-food-loss-waste/en/
    """
    food_waste_coef = {
    # Meat 6
    "Beef": 100,
    "Lamb": 100,
    "Chicken": 50,
    "Pork": 80,
    "Turkey": 70,

     # Seafood 6
    "Fish": 40,
    "Shrimp": 60,
    "Crab": 60,
    "Oyster": 50,
    "Lobster": 80,
    "Clams": 50,

    # Dairy Products 11
    "Eggs": 30,
    "Milk": 50,
    "Yogurt": 50,
    "Butter": 60,
    "Cheddar Cheese": 70,
    "Mozzarella Cheese": 70,
    "Swiss Cheese": 70,
    "Parmesan Cheese": 80,
    "Cream Cheese": 70,
    "Brie Cheese": 80,
    "Gouda Cheese": 80,

    # Fruits 27 
    "Apple": 10,
    "Banana": 5,
    "Grapes": 10,
    "Pineapple": 15,
    "Orange": 10,
    "Lemon": 10,
    "Pear": 10,
    "Peach": 10,
    "Strawberry": 10,
    "Blueberry": 10,
    "Cherry": 10,
    "Raspberry": 10,
    "Watermelon": 20,
    "Melon": 20,
    "Kiwi": 10,
    "Mango": 15,
    "Papaya": 15,
    "Fig": 15,
    "Plum": 10,
    "Pomegranate": 20,
    "Date": 10,
    "Olives": 10,
    "Avocado": 15,
    "Berry": 10,
    "Cherries": 10,
    "Grapefruit": 15,
    "Nectarines": 15,
    
    # Vegetables and Herbs 23    
    "Cabbage": 10,
    "Spinach": 5,
    "Kale": 5,
    "Lettuce": 5,
    "Broccoli": 15,
    "Carrot": 10,
    "Zucchini": 5,
    "Asparagus": 10,
    "Cauliflower": 10,
    "Bell Pepper": 15,
    "Cucumber": 5,
    "Pumpkin": 15,
    "Tomato": 10,
    "Peas": 10,
    "Squash": 10,
    "Celery": 5,
    "Mushrooms": 15,
    "Onions": 5,
    "Peppers": 10,
    "Garlic": 5,
    "Chili": 10,
    "Herbs": 5,
    "Coriander": 5,

    # Grains and Cereals
    "Rice": 30,
    "Wheat": 20,
    "Barley": 20,
    "Oats": 15,
    "Corn": 20,
    "Couscous": 20,
    "Polenta": 20,
    "Rye": 20,
    "Brown Rice": 30,
    "White Rice": 30,
    "Tortillas": 20,
    "Noodles": 20,
    "Granola": 30,
    "Oatmeal": 20,
    "Crackers": 20,
    "Popcorn": 20,
    "Cereal": 20,
    "Pasta": 20,
    "Black Beans": 10,
    "Kidney Beans": 10,
    "Soybeans": 15,
    "Chickpeas": 15,
    "Lentils": 10,
    
    # Legumes and Beans 12
    "Peanuts": 20,
    "Almonds": 10,
    "Cashews": 10,
    "Pistachios": 10,
    "Walnuts": 10,
    "Hazelnuts": 10,
    "Sunflower Seeds": 10,
    "Chia Seeds": 10,
    "Flax Seeds": 10,
    "Olive Oil": 5,
    "Coconut Oil": 5,
    "Butter": 10,


    # Nuts and Seeds 8
    "Almonds": 10,
    "Cashews": 10,
    "Pistachios": 10,
    "Walnuts": 10,
    "Hazelnuts":10,
    "Sunflower Seeds": 10,
    "Chia Seeds": 10,
    "Flax Seeds": 10,

    # Oils and Fats
    "Olive Oil": 5,
    "Coconut Oil": 5,
    "Butter": 5,
    "Ghee": 5,
    "Margarine": 5,

    # Bakery and Confectionery
    "Bread": 10,
    "Cakes": 20,
    "Pastries": 20,
    "Cookies": 20,
    "Muffins": 20,
    "Donuts": 20,
    "Brownies": 20,
    "Bagels": 10,    

    "Frozen Meals": 3.5,
    "Canned Goods": 1.1,
    "Snacks": 1.2,
    "Salami": 12.0,
    "Bologna": 12.0,
    "Sausage": 12.0,
    "Bacon": 8.0,

    # Beverages
    "Juice": 10,
    "Coffee": 15,
    "Tea": 10,
    "Soda": 20,
    "Smoothies": 15,
    "Energy drink": 20,
    "Beer": 25,
    "Wine": 20,
    "Vodka": 30,
    "Whiskey": 30,
    "Rum": 30,
    "Tequila": 30,
    "Champagne": 25
    }
    """
    Retrieve the carbon footprint of a food item.
    If the food item doesn't exist, return None.
    """
    @classmethod
    def get_carbon_coef(cls, food_name):
        return cls.food_CarbonFootPrint_coef.get(food_name)
    @classmethod
    def get_waste_coef(cls, food_name):
        return cls.food_waste_coef.get(food_name)


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

    # Total CO2 Footprint = CO2 Footprint of producing the Food + CO2 Footprint of the Waste
    # from the decomposition of bio material if the waste is not recycled.
    # The waste produces methane gas CH4 which has 25X impact compering to CO2
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

"Stuff for pushing local articles into green guides"

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_published = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
