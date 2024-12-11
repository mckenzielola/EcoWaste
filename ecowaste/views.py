import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from . import models
from .models import FoodDatabase, ImpactCalculator, WasteItem, Item
from .forms import WasteItemForm, PerishableItemForm
from django.shortcuts import render
from datetime import datetime, timedelta, timezone
from .models import Article
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count

@login_required
def home(request):
    perishable_items = Item.objects.filter(author=request.user).order_by('expiration')
    waste_items = WasteItem.objects.filter(user=request.user)

    # retrieve the items to render to the home.html
    context = {
        'perishable_items' : perishable_items,
        'waste_items' : waste_items
    }
    # retrieve all of the perishables created by the user
    # items = models.Item.objects.all()
    # send http request to render home html page
    return render(request, "ecowaste/home.html", context)

def about(request):
# send http request to render about html page
    return render(request, "ecowaste/about.html")

@login_required
def freshness_tracker(request):
    if request.method == 'POST':
        form = PerishableItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.author = request.user
            item.save()
            return redirect('ecowaste-freshness-tracker')
    else:
        form = PerishableItemForm()

    items = Item.objects.filter(author=request.user).order_by('expiration')
    context = {
        'form' : form,
        'items' : items
    }
    # send http request to render freshness tracker html page
    return render(request, "ecowaste/freshness-tracker.html", context)

def waste_tracker(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = WasteItemForm(request.POST)
            if form.is_valid():
                waste_item = form.save(commit=False)
                waste_item.user = request.user
                waste_item.save()
                return redirect('ecowaste-waste-tracker')
        else:
            form = WasteItemForm()
        waste_items = WasteItem.objects.filter(user=request.user)
    else:
        form = WasteItemForm()

    user_waste_count = WasteItem.objects.filter(user=request.user).count()

    all_users_waste_count = WasteItem.objects.values('user').annotate(count=Count('id')).order_by('count')

    total_users = len(all_users_waste_count)

    lower_percentile = 100 * sum(1 for x in all_users_waste_count if x['count'] < user_waste_count) / total_users

    waste_items = WasteItem.objects.filter(user=request.user)

    return render(request, "ecowaste/waste-tracker.html", {
        'form': form,
        'waste_items': waste_items,
        'percentile': lower_percentile,
    })

def delete_waste_item(request, waste_item_id):
    waste_item = get_object_or_404(WasteItem, id=waste_item_id)

    if request.method == 'POST':
        waste_item.delete()
        return redirect('ecowaste-waste-tracker')  

    return redirect('ecowaste-waste-tracker') 


def impact_calculator(request):
    return render(request, "ecowaste/impact-calculator.html")

def green_guides(request):
    articles = Article.objects.all().order_by('-date_published')  # Fetch and order by date
    return render(request, "ecowaste/green-guides.html", {'articles': articles})

def article_detail(request, id):
    article = Article.objects.get(pk=id)
    return render(request, "ecowaste/article-detail.html", {'article': article})

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

    return render(request, "ecowaste/impact-calculator.html", {'range': range}, context)

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