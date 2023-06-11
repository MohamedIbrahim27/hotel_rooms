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
def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and accout_actvation_token.check_token(user, token):
        # activate the user's account
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated!')
        login(request, user)
        return redirect('/')
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('/')
def signup(request):
    if request.method == 'POST' and 'signup' in request.POST:
        first_name=None
        email=None
        password=None
        passwordconfigration=None
        
        if 'first_name' in request.POST : first_name=request.POST['first_name']
        else :messages.error(request,'Error in First Name !')
        
        if 'email' in request.POST : email=request.POST['email']
        else : messages.error(request,'Error in Email !')
        
        if 'password' in request.POST: password=request.POST['password']
        else : messages.error(request,'Error in password !')
        
        if 'passwordconfigration' in request.POST: passwordconfigration=request.POST['passwordconfigration']
        else : messages.error(request,'Error in Password Configration !')
        context={'first_name':first_name,
                'email':email}
        if first_name and email and password and passwordconfigration:
            if User.objects.filter(email=email).exists():
                messages.error(request,'This Email Name is taken !')
                return render(request,'registration/signup.html',context)
            else:
                if password != passwordconfigration:
                    messages.error(request,'The two password fields didn’t match.')
                    return render(request,'registration/signup.html',context)
                else:
                    username = email.split("@")[0]
                    user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    is_active=False,
                    email=email,
                    password=password
                    )
                    user.save()
        else:
            messages.error(request,'Please fill in all fields !')
            return render(request,'registration/signup.html',context)
        mailsubject='activate your account'
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = accout_actvation_token.make_token(user)
        message=f"Hi {user.username},\n\nPlease click on the following link to activate your account:\n\n{get_current_site(request).domain}/accounts/activate_account/{uid}/{token}/\n\nThanks!\n"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email,] 
        emailmessage=send_mail(mailsubject,message,email_from,recipient_list)
        
        if emailmessage:
            messages.success(request,f'User has been registered successfully , go to {email} to activate your account ! ')
            return redirect('/accounts/signin')
        else:
            messages.error(request,f'filed to send email to  {email} ! ')
            return redirect('/accounts/signup')
    else:
        return render(request,'registration/signup.html')


def signin(request):
    if request.method == 'POST':
        # email = request.POST.get('email')
        # password = request.POST.get('password')
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Go to'+email+'to active your account !')
                return redirect('/accounts/signin')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('/accounts/signin')
    else:
        return render(request, 'registration/signin.html')

def log_out(request):
    context ={'log_out' : log_out}
    return render(request, 'registration/log_out.html',context)

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
def edit_profile(request ,slug):
    profile=get_object_or_404(Profile,slug=slug)
    if request.user.id == profile.user.id:
        country_list = list(countries)
        if request.method == 'POST':
            if request.user is not None:
                user_profile = Profile.objects.get(user=request.user)
                context={
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'email': request.user.email,
                    'image':user_profile.image,
                    'phone': user_profile.phone,
                    'country': user_profile.country,
                    'country_list': country_list,
                    'adress': user_profile.adress,
                }
                if request.POST['first_name'] and request.POST['last_name'] and request.POST['email'] and request.POST['phone'] and request.POST['country']  and request.POST['adress']:
                    request.user.first_name= request.POST['first_name']
                    request.user.last_name= request.POST['last_name']
                    if request.POST['email'] != request.user.email:
                        if User.objects.filter(email=request.POST['email']).exists():
                            messages.error(request, 'Email is already taken.')
                            return render(request, 'editprofile.html', context)
                        request.user.email = request.POST['email']
                    user_profile.phone= request.POST['phone']
                    if 'country' in request.POST:
                        user_profile.country = request.POST['country']
                    user_profile.adress= request.POST['adress']
                    request.user.save()
                    user_profile.save()
                    messages.success(request,'Your Data Has Been Saved')
                    context1={
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'email': request.user.email,
                    'image':user_profile.image,
                    'phone': user_profile.phone,
                    'country': user_profile.country,
                    'country_list': country_list,
                    'adress': user_profile.adress,
                    }
                    slug = user_profile.slug
                    return redirect ('/accounts/profile/' +slug+ '/editprofile')
                else:
                    messages.error(request,'Please fill in all fields !')
                    return render(request, 'editprofile.html',context)
            return render(request, 'editprofile.html',context)
        else:
            if request.user is not None:
                user_profile = Profile.objects.get(user=request.user)
                context={
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'email': request.user.email,
                    'image':user_profile.image,
                    'phone': user_profile.phone,
                    'country': user_profile.country,
                    'country_list': country_list,
                    'adress': user_profile.adress,
                }
            return render(request, 'editprofile.html',context)
    else:
        return HttpResponseForbidden("You don't have permission to edit this profile.")



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