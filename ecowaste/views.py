from django.shortcuts import render, HttpResponse

def home(request):
    # send http request to render home html page
    return render(request, "ecowaste/home.html")

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
