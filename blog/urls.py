from unicodedata import name
from django.urls import path ,include
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from.api_view import *
app_name='blog'


urlpatterns = [
    path('',BlogList.as_view(),name='post_list'),
    path('<slug:slug>',BlogDetail.as_view(),name='post_detail'),
    path('category/<str:slug>',PostByCategory.as_view(),name='category'),
    path('tag/<str:slug>',PostByTags.as_view(),name='tag'),
    
    
    # api
    
    path('api/list',post_list_api,name='post_list_api'),
    path('api/list/<int:id>',post_details_api,name='post_details_api'),
    path('api/list/filter/<str:query>',post_search_api,name='post_search_api'),
]
