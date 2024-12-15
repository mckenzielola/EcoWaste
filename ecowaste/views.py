import json
import random
from django.shortcuts import render, redirect
from .models import FoodDatabase, ImpactCalculator, WasteItem, Item
from .forms import WasteItemForm, PerishableItemForm
from django.shortcuts import render
from .models import Article
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from datetime import datetime, timedelta
from .forms import WasteItemForm
from dateutil.parser import parse as parse_date

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



def calculate_co2_impact(request):
    # Ensure user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

    # Use the authenticated user
    user = request.user
    period = request.GET.get('period')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Validate date inputs
    try:
        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)
    except ValueError:
        return JsonResponse({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

    if not start_date or not end_date:
        return JsonResponse({"error": "Invalid range type or missing dates."}, status=400)

    gram_to_kg = 0.001
    food_impactList = {}
    waste_impactList = {}
    total_impactList = {}
    food_categories = {}

    # Calculate food impact by time
    food_list = Item.objects.filter(author=user, date_added__range=[start_date, end_date])
    for food in food_list:
        time = food.date_added.strftime('%Y-%m-%d') if period == "past-month" else food.date_added.strftime('%Y-%m')
        carbon_coef = FoodDatabase.get_carbon_coef(food.perishable)
        if carbon_coef:
            coef = float(carbon_coef)
            quantity = float(food.quantity)
            food_impact = round(coef * quantity * gram_to_kg, 2)
            food_impactList[time] = food_impactList.get(time, 0) + food_impact
            
            # Add impact to category total
            category = get_waste_item_category(food.perishable)
            food_categories[category] = food_categories.get(category, 0) + food_impact
    print('waste')
    # Calculate waste impact by time
    waste_list = WasteItem.objects.filter(user=user, date_added__range=[start_date, end_date])
    for waste_item in waste_list:
        time = waste_item.date_added.strftime('%Y-%m-%d') if period == "past-month" else waste_item.date_added.strftime('%Y-%m')
        carbon_coef = FoodDatabase.get_waste_coef(waste_item.name)
        if carbon_coef:
            coef = float(carbon_coef)
            quantity = float(waste_item.quantity)
            waste_impact = round(coef * quantity * gram_to_kg, 2)
            waste_impactList[time] = round(waste_impactList.get(time, 0) + waste_impact,2)

            category = get_waste_item_category(waste_item.name)
            food_categories[category] = round(food_categories.get(category, 0) + waste_impact,2)

    # Combine both food and waste impacts and compute cumulative daily totals
    period = sorted(set(food_impactList.keys()).union(set(waste_impactList.keys())))

    total_impactList = {}
    cumulative_total = 0

    for time in period:
        food_impact = food_impactList.get(time, 0)
        waste_impact = waste_impactList.get(time, 0)
        current_total = food_impact + waste_impact
        
        cumulative_total += current_total
        total_impactList[time] = round(cumulative_total,2)
            
    return JsonResponse({
        'food_categories': food_categories,
        'total_impactList': total_impactList,
        'food_impactList': food_impactList,
        'waste_impactList': waste_impactList,
        'start_date': start_date,
        'end_date': end_date,
    })

def get_waste_item_category(waste_item_name):
    # Iterate through the food categories
    for category, items in WasteItemForm.FOOD_CATEGORIES:
        if waste_item_name in items:
            return category
    return "Uncategorized"  # Return 'Uncategorized' if not found