from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView ,DetailView
from django.contrib.auth.models import User
from.models import *
from property.models import Place,Property,Category
from django.views.generic.edit import FormMixin
from django.core.exceptions import ValidationError
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from blog.models import Post

# Create your views here.



def show_home(request):
    # distinct() ==>  method can be used to filter out those duplicates and 
    # ensure that each object appears only once in the queryset.
    """
        By specifying property_place__isnull=False, you are retrieving only those Place 
        objects that have at least one associated property. This means you are excluding
        any Place objects that do not have any associated properties from the queryset.
    """
    places=Place.objects.filter(property_place__isnull=False).distinct().annotate(property_count=Count('property_place'))
    tour_packages=Property.objects.all()[:5]
    category=Category.objects.filter(croperty_category__isnull=False).distinct() 
    restaurant=Property.objects.filter(name__icontains='Restaurant')
    recent_posts= Post.objects.all()[:4]
    return render(request,'settings/home.html',{
        'places':places,
        'tour_packages':tour_packages,
        'category':category,
        'restaurant':restaurant,
        'recent_posts':recent_posts,
    })


def home_search(request):
    q=request.GET.get('q','')
    place=request.GET.get('place','')
    object_list=Property.objects.filter(
                Q(name__icontains=q)&
                Q(place__name__icontains=place)|
                Q(place__isnull=True))
    
    return render(request,'settings/search_home.html',{
        'object_list':object_list,
    })


def category_filter(request,category):
    category=Category.objects.get(name=category)
    object_list=Property.objects.filter(category=category)
    return render(request,'settings/search_home.html',{
        'object_list':object_list,
    })
    
    
def featured_destination(request,name):
    
    object_list=Property.objects.filter(name=name)
    return render(request,'settings/search_home.html',{
        'object_list':object_list,
    })
    
def contact_us(request):
    return render(request,'settings/contact.html')