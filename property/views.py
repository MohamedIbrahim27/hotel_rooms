from django.shortcuts import render
from django.views.generic import ListView ,DetailView ,CreateView
from django.contrib.auth.models import User
from.models import *
from django.views.generic.edit import FormMixin
from django.core.exceptions import ValidationError
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
# Create your views here.


class PropertyList(ListView):
    model = Property
    paginate_by = 4

    def get_queryset(self):# fiter to get property by place and country ?
        place = self.request.GET.get('place')
        country = self.request.GET.get('country')
        queryset = Property.objects.all()
        if place:
            place = get_object_or_404(Place, name=place)
            queryset = queryset.filter(place=place)
        if country:
            queryset = queryset.filter(place__country=country)
        return queryset


def show_home(request):
    return render(request,'property/home.html')

class PropertyDetail(DetailView):
    model=Property
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context["filter_by_room"] = Property.objects.filter(name__icontains="Room").exclude(pk=category.pk)[:3]
        context["related"] = Property.objects.filter(category=category.category).exclude(pk=category.pk)[:3] # get lat frist 3 property i was add except post iam in now 
        context["count_choices_gu"] = PropertyBook.COUNTGU # this is a name ''count_choices_gu'' to be able to loop on it in templates .
        context["count_choices_ch"] = PropertyBook.COUNTCH # this is a name ''count_choices_ch'' to be able to loop on it in templates .
        return context
    def post(self,request,*args, **kwargs):
        date_from=None  
        date_to=None 
        guest=None
        children=None
        if request.method=='POST': # this def to add property book 
            date_from = request.POST.get('date_from')
            date_to = request.POST.get('date_to')
            guest = request.POST.get('guest')
            children = request.POST.get('children')
            date_obj = datetime.strptime(date_from, '%m/%d/%Y') #change format for date from 5/31/2023 to 2023-05-17
            formatted_date1 = date_obj.strftime('%Y-%m-%d')
            date_obj = datetime.strptime(date_to, '%m/%d/%Y')
            formatted_date2 = date_obj.strftime('%Y-%m-%d')
            booking = PropertyBook(
                user=request.user,
                property=self.get_object(),
                date_from=formatted_date1,
                date_to=formatted_date2,
                guest=guest,
                children=children
            )
            booking.save()
            return super().get(request, *args, **kwargs)


class PropertyCreate(LoginRequiredMixin,CreateView):
    model = Property
    fields=['name','image','price','description','place','category']
    success_url=reverse_lazy('property:property_list')
    def form_valid(self, form):
        form.instance.user =self.request.user
        return super(PropertyCreate,self).form_valid(form)