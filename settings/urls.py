from unicodedata import name
from django.urls import path ,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name='settings'


urlpatterns = [
    path('',views.show_home,name='home'),
    path('search',views.home_search,name='home_search'),
    path('search/<slug:category>',views.category_filter,name='category_filter'),
    path('search',views.featured_destination,name='featured_destination'),
    path('contact_us',views.contact_us,name='contact_us'),
]
