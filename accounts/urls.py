from unicodedata import name
from django.urls import path ,include
from . import views
from.views import Login ,Regiser
from django.conf import settings
from django.conf.urls.static import static
app_name='accounts'


urlpatterns = [
    # path('signup',views.signup ,name='signup'),
    # path('signin',views.signin ,name='signin'),
    path('login/',Login.as_view(),name='login'),
    path('register/',Regiser.as_view(),name='register'),
    # path('activate_account/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('log_out',views.log_out ,name='log_out'),
    path('profile/<slug:slug>',views.profile ,name='profile'),
    path('profile/<slug:slug>/editprofile',views.edit_profile ,name='edit'),
    path('remove_myresevation/<int:resevation_id>',views.remove_myresevation ,name='remove_myresevation'),
    path('remove_mylisting/<int:property_id>',views.remove_mylisting ,name='remove_mylisting'),
]
