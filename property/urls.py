from unicodedata import name
from django.urls import path ,include
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static
from.api_view import *
app_name='property'


urlpatterns = [
    # path('hotel/search',views.search,name='search'),
    path('hotel/',PropertyList.as_view(),name='property_list'),
    path('hotel/<slug:slug>',PropertyDetail.as_view(),name='property_detail'),
    
    
    # api
    path('property/list',PropertyAPiList.as_view(),name='PropertyAPiList'),
    path('property/list/<int:pk>',PropertyAPiDetail.as_view(),name='PropertyAPiDetail'),
]
