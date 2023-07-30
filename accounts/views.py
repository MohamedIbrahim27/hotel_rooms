from django.contrib import messages
from django.shortcuts import render ,redirect ,get_object_or_404

from.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login ,authenticate
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django_countries import countries
from.tokens import accout_actvation_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from property.models import PropertyBook,Property
from project import settings
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from.forms import SignupForm
from django.contrib.auth import logout

class Login(LoginView):
    template_name='registration/login.html'
    fields='__all__'
    redirect_authenticated_user=True
    def get_success_url(self):
        return reverse_lazy('settings:home')
    
class Regiser(FormView):
    template_name='registration/register.html'
    form_class=SignupForm
    redirect_authenticated_user=True
    success_url=reverse_lazy('property:property_list')
    def form_valid(self, form):
        user = form.save(commit=False)
        email = form.cleaned_data.get('email')
        username = email.split("@")[0]  
        user.username = username 
        user.save()
        if user is not None:
            login(self.request,user)
        return super(Regiser,self).form_valid(form)
    
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('property:property_list')
        return super(Regiser,self).get(*args, **kwargs)
    
def log_out(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/accounts/login/')
def profile(request,slug):
    profile=get_object_or_404(Profile,slug=slug)
    my_resevation=PropertyBook.objects.filter(user=profile.user)
    my_listings=Property.objects.filter(user=profile.user)
    if request.user.id == profile.user.id:
        context={'profile':profile,
                    'my_resevation':my_resevation,
                    'my_listings':my_listings}
        return render(request,'profile.html',context)
    else:
        return HttpResponseForbidden("You don't have permission to view this profile.")

@login_required(login_url='/accounts/login/')
def edit_profile(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    if request.user.id == profile.user.id:
        country_list = list(countries)
        user_profile = Profile.objects.get(user=request.user)

        if request.method == 'POST':
            form_data = request.POST  # Get form data from POST
            image_file = request.FILES.get('image', None)  # Get uploaded image file

            if form_data['first_name'] and form_data['last_name'] and form_data['email'] and form_data['phone'] and form_data['country'] and form_data['adress']:
                if image_file:
                    user_profile.image = image_file  # Assign the uploaded image file
                request.user.first_name = form_data['first_name']
                request.user.last_name = form_data['last_name']

                if form_data['email'] != request.user.email:
                    if User.objects.filter(email=form_data['email']).exists():
                        messages.error(request, 'Email is already taken.')
                        return render(request, 'editprofile.html', context)
                    request.user.email = form_data['email']

                user_profile.phone = form_data['phone']
                user_profile.country = form_data['country']
                user_profile.adress = form_data['adress']
                request.user.save()
                user_profile.save()
                messages.success(request, 'Your Data Has Been Saved')
                return redirect('/accounts/profile/' + slug + '/editprofile')
            else:
                messages.error(request, 'Please fill in all fields !')
                return render(request, 'editprofile.html', context)
        
        # If it's a GET request
        context = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'image': user_profile.image,
            'phone': user_profile.phone,
            'country': user_profile.country,
            'country_list': country_list,
            'adress': user_profile.adress,
        }
        return render(request, 'editprofile.html', context)
    else:
        return HttpResponseForbidden("You don't have permission to edit this profile.")
    
    
# def edit_profile(request ,slug):
#     profile=get_object_or_404(Profile,slug=slug)
#     if request.user.id == profile.user.id:
#         country_list = list(countries)
#         if request.method == 'POST':
#             if request.user is not None:
#                 user_profile = Profile.objects.get(user=request.user)
#                 context={
#                     'first_name': request.user.first_name,
#                     'last_name': request.user.last_name,
#                     'email': request.user.email,
#                     'image':user_profile.image,
#                     'phone': user_profile.phone,
#                     'country': user_profile.country,
#                     'country_list': country_list,
#                     'adress': user_profile.adress,
#                 }
#                 if request.POST['first_name'] and request.POST['last_name'] and request.POST['email'] and request.POST['phone'] and request.POST['country']  and request.POST['adress']:
#                     request.user.first_name= request.POST['first_name']
#                     request.user.last_name= request.POST['last_name']
#                     if request.POST['email'] != request.user.email:
#                         if User.objects.filter(email=request.POST['email']).exists():
#                             messages.error(request, 'Email is already taken.')
#                             return render(request, 'editprofile.html', context)
#                         request.user.email = request.POST['email']
#                     user_profile.phone= request.POST['phone']
#                     if 'country' in request.POST:
#                         user_profile.country = request.POST['country']
#                     user_profile.adress= request.POST['adress']
#                     request.user.save()
#                     user_profile.save()
#                     messages.success(request,'Your Data Has Been Saved')
#                     context1={
#                     'first_name': request.user.first_name,
#                     'last_name': request.user.last_name,
#                     'email': request.user.email,
#                     'image':user_profile.image,
#                     'phone': user_profile.phone,
#                     'country': user_profile.country,
#                     'country_list': country_list,
#                     'adress': user_profile.adress,
#                     }
#                     slug = user_profile.slug
#                     return redirect ('/accounts/profile/' +slug+ '/editprofile')
#                 else:
#                     messages.error(request,'Please fill in all fields !')
#                     return render(request, 'editprofile.html',context)
#             return render(request, 'editprofile.html',context)
#         else:
#             if request.user is not None:
#                 user_profile = Profile.objects.get(user=request.user)
#                 context={
#                     'first_name': request.user.first_name,
#                     'last_name': request.user.last_name,
#                     'email': request.user.email,
#                     'image':user_profile.image,
#                     'phone': user_profile.phone,
#                     'country': user_profile.country,
#                     'country_list': country_list,
#                     'adress': user_profile.adress,
#                 }
#             return render(request, 'editprofile.html',context)
#     else:
#         return HttpResponseForbidden("You don't have permission to edit this profile.")



def remove_myresevation(request,resevation_id):
    property=PropertyBook.objects.get(id=resevation_id)
    property.delete()
    user_profile = Profile.objects.get(user=request.user)
    slug = user_profile.slug
    return redirect ('/accounts/profile/' +slug)

def remove_mylisting(request,property_id):
    property=Property.objects.get(id=property_id)
    property.delete()
    user_profile = Profile.objects.get(user=request.user)
    slug = user_profile.slug
    return redirect ('/accounts/profile/' +slug)