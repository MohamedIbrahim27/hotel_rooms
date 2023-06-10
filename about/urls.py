from unicodedata import name
from django.urls import path ,include
from.views import *
from django.conf import settings
from django.conf.urls.static import static
app_name='about'


urlpatterns = [
    path('',AboutList.as_view(),name='about_list'),
]
