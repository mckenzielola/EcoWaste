import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from . import models
from .models import FoodDatabase, ImpactCalculator, WasteItem
from .forms import WasteItemForm
from django.shortcuts import render
from datetime import datetime, timedelta, timezone

def home(request):
    items = models.Item.objects.all()
    context = {
        'items': items
    }
    # retrieve all of the perishables created by the user
    # items = models.Item.objects.all()
    # send http request to render home html page
    return render(request, "ecowaste/home.html", context)

def about(request):
# send http request to render about html page
    return render(request, "ecowaste/about.html")

def freshness_tracker(request):
# send http request to render freshness tracker html page
    return render(request, "ecowaste/freshness-tracker.html")

def waste_tracker(request):
# send http request to render waste tracker html page
    if request.method == 'POST':
        form = WasteItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ecowaste-waste-tracker')
    else:
        form = WasteItemForm()

    waste_items = WasteItem.objects.all()
    return render(request, "ecowaste/waste-tracker.html", {'form': form, 'waste_items': waste_items})


def impact_calculator(request):
    return render(request, "ecowaste/impact-calculator.html")

def green_guides(request):
    return render(request, "ecowaste/green-guides.html")

def eco_waste_view(request):
    user = request.user

    # Define the date ranges for the impact data
    today = timezone.now().date()
    last_week = today - timedelta(days=7)
    last_month = today - timedelta(days=30)
    last_quarter = today - timedelta(days=90)
    last_year = today - timedelta(days=365)

    # Initialize the Impact calculator for the logged-in user
    impact_calculator = ImpactCalculator(user)
    
    # Set date range for each category and calculate the impact
    impact_calculator.set_date_range(last_week, today)
    co2_past_week = calculate_impact(impact_calculator.get_food_data())
    waste_past_week = calculate_waste_impact(impact_calculator.get_waste_data())

    impact_calculator.set_date_range(last_month, today)
    co2_past_month = calculate_impact(impact_calculator.get_food_data())
    waste_past_month = calculate_waste_impact(impact_calculator.get_waste_data())

    impact_calculator.set_date_range(last_quarter, today)
    co2_past_quarter = calculate_impact(impact_calculator.get_food_data())
    waste_past_quarter = calculate_waste_impact(impact_calculator.get_waste_data())

    impact_calculator.set_date_range(last_year, today)
    co2_past_year = calculate_impact(impact_calculator.get_food_data())
    waste_past_year = calculate_waste_impact(impact_calculator.get_waste_data())

    context = {
        'co2_past_week': co2_past_week,
        'waste_past_week': waste_past_week,
        'co2_past_month': co2_past_month,
        'waste_past_month': waste_past_month,
        'co2_past_quarter': co2_past_quarter,
        'waste_past_quarter': waste_past_quarter,
        'co2_past_year': co2_past_year,
        'waste_past_year': waste_past_year,
    }

    return render(request, "ecowaste/impact-calculator.html", {'range': range})

def calculate_impact(food_data):
    """Calculate the total carbon footprint of consumed food items."""
    total_impact = 0
    for food_name, quantity in food_data:
        carbon_footprint = FoodDatabase.get_carbon_footprint(food_name)
        if carbon_footprint:
            total_impact += carbon_footprint * quantity  # Assuming quantity is in kg
    return total_impact

def calculate_waste_impact(waste_data):
    """Calculate the total waste impact."""
    total_waste = 0
    for waste_item in waste_data:
        # Assuming quantity is in kilograms (or appropriate unit), adjust calculation as needed
        total_waste += float(waste_item.quantity)
    return total_waste

def calculate_co2_impact(request, range):
    # Your logic for CO2 calculation here
    return render(request, 'ecowaste/impact_result.html', {'range': range})

def calculate_waste_impact(request, range):
    # Your logic for waste calculation here
    return render(request, 'ecowaste/impact_result.html', {'range': range})