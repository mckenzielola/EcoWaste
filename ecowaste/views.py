from django.shortcuts import render, HttpResponse
from . import models


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
    return render(request, "ecowaste/waste-tracker.html")

def impact_calculator(request):
# send http request to render impactcalculator html page
    return render(request, "ecowaste/impact-calculator.html")

def green_guides(request):
# send http request to render green guides html page
    return render(request, "ecowaste/green-guides.html")
