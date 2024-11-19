from django.urls import path
from . import views

'app/model_viewtype'
'ecowaste/item_detail.html'

urlpatterns = [
    path('', views.PerishableListView.as_view(), name="ecowaste-home"),
    path('ecowaste/<int:pk>/', views.PerishableDetailView.as_view(), name="ecowaste-detail"),
    path('about/', views.about, name="ecowaste-about"),
    path('freshness-tracker/', views.freshness_tracker, name="ecowaste-freshness-tracker"),
    path('waste-tracker/', views.waste_tracker, name="ecowaste-waste-tracker"),
    path('impact-calculator/', views.impact_calculator, name="ecowaste-impact-calculator"),
    path('green-guides/', views.green_guides, name="ecowaste-green-guides"),
]
