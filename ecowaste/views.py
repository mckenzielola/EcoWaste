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

    # check if users greater than 0
    if total_users > 0:

        lower_percentile = 100 * sum(1 for x in all_users_waste_count if x['count'] < user_waste_count) / total_users
    else:
        lower_percentile = 0 #when there are no users

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

@login_required
def calculate_co2_impact(request):
    # Get the current user
    user = request.user
    today = timezone.now().date()

    # Define time ranges
    time_ranges = {
        'past-week': (today - timedelta(days=7), today),
        'past-month': (today - timedelta(weeks=4), today),
        'past-quarter': (today - timedelta(weeks=12), today),
        'past-year': (today - timedelta(weeks=52), today)
    }

    # Initialize results dictionary
    impact_results = {}

    # Calculate impact for each time range
    for range_name, (start_date, end_date) in time_ranges.items():
        # Create Impact Calculator
        impact_calculator = ImpactCalculator(user, (start_date, end_date))
        
        # Get food and waste data
        food_data = impact_calculator.get_food_data()
        waste_data = impact_calculator.get_waste_data()
        
        # Calculate food impact
        food_impact = 0
        food_details = []
        for food, quantity in food_data:
            carbon_coef = FoodDatabase.get_carbon_coef(food)
            if carbon_coef:
                # Convert quantity to pounds
                weight_in_pounds = quantity * 2.20462
                food_impact += round(carbon_coef * weight_in_pounds, 3)
                food_details.append({
                    'name': food,
                    'quantity': quantity,
                    'carbon_impact': round(carbon_coef * weight_in_pounds, 3)
                })
        print(food_impact)
        
        # Calculate waste impact
        waste_impact = 0
        waste_details = []
        for waste_item in waste_data:
            carbon_coef = FoodDatabase.get_waste_coef(waste_item.name)
            if carbon_coef:
                waste_impact += round(carbon_coef * waste_item.quantity, 3)
                waste_details.append({
                    'name': waste_item.name,
                    'quantity': waste_item.quantity,
                    'carbon_impact': round(carbon_coef * waste_item.quantity, 3)
                })
        print(waste_impact)
        # Store results for this time range
        impact_results[range_name] = {
            'food_impact': food_impact,
            'waste_impact': waste_impact,
        }

    # Render template with results
    return render(request, 'ecowaste/impact-calculator.html', {
        'total_food_impact': sum(results['food_impact'] for results in impact_results.values()),
        'total_waste_impact': sum(results['waste_impact'] for results in impact_results.values())
    })