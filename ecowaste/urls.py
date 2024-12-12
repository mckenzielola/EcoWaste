from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name="ecowaste-home"),
    path('about/', views.about, name="ecowaste-about"),
    path('freshness-tracker/', views.freshness_tracker, name="ecowaste-freshness-tracker"),
    path('waste-tracker/', views.waste_tracker, name="ecowaste-waste-tracker"),
    path('delete_waste_item/<int:waste_item_id>/', views.delete_waste_item, name='delete_waste_item'),
    path('impact-calculator/', views.impact_calculator, name="ecowaste-impact-calculator"),
    
    path('green-guides/', views.green_guides, name="ecowaste-green-guides"),
    path('green-guides/<int:id>/', views.article_detail, name='article-detail'),
  
   
    path('calculate-impact/<str:type>/<str:range>/', views.calculate_co2_impact, name='calculate_co2_range'),
    path('calculate-impact/co2/custom/<str:start_date>/<str:end_date>/', views.calculate_co2_impact, name='calculate_co2_custom_impact'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
