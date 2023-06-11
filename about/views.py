from django.views.generic import ListView ,DetailView
from.models import *
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

# Create your views here.

class AboutList(ListView):
    model=FAQ
    template_name='about/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["about"] = About.objects.last()
        return context
    
