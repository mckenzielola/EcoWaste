from django.shortcuts import render, HttpResponse, redirect
from . import models
from .models import WasteItem
from .forms import WasteItemForm
from django.views.generic import ListView, DetailView

def home(request):
    items = models.Item.objects.all()
    context = {
        'items': items
    }
    # retrieve all of the perishables created by the user
    # items = models.Item.objects.all()
    # send http request to render home html page
    return render(request, "ecowaste/home.html", context)


class PerishableListView(ListView):
    model = models.Item
    template_name = 'ecowaste/home.html'
    context_object_name = 'items'

class PerishableDetailView(DetailView):
    model = models.Item

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
# send http request to render impactcalculator html page
    return render(request, "ecowaste/impact-calculator.html")

def green_guides(request):
# send http request to render green guides html page
    return render(request, "ecowaste/green-guides.html")
