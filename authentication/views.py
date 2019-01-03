from django.shortcuts import render,redirect,reverse
from  django.http import  JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from .forms import RegisterForm
from django.contrib.auth import get_user_model
from django.views.generic import DetailView
User = get_user_model()
# Create your views here.
def register(request,*args,**kwargs):
    if request.method=='POST':
        username_exists = User.objects.filter(username=request.POST.get('username')).exists()
        mail_exists = User.objects.filter(email=request.POST.get('email')).exists()
        passwords_match = request.POST.get('password1')==request.POST.get('password2')
        if username_exists or mail_exists or not passwords_match:
            form = RegisterForm(request.POST, request.FILES)
            print(form.errors)
            return JsonResponse({
                'status':1,
                'error_data':{
                    'username_exists':username_exists,
                    'email_exists':mail_exists,
                    'passwords_match':passwords_match
                 }
            })
        else:
            print("POST",request.POST)
            print("Files",request.FILES)
            form = RegisterForm(request.POST,request.FILES)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password1"]
                form.save()
                user = authenticate(username=username, password=password)
                login(request, user)
                return JsonResponse({
                    'status':0,
                    'data':{
                        'redirect_url':request.build_absolute_uri('/')
                    }
                })
            else:
                return JsonResponse({
                    'status': 1,
                    'error_data': {
                        'errors_list':form.errors
                    }
                })

    else:
        context = {'form': RegisterForm()}
        return render(request,'registration/register.html',context)
def userlogout(request,*args,**kwargs):
    logout(request)
    return  render(request,'registration/logout.html')
class UserProfile(DetailView):
    model = User
    template_name = 'registration/userpage.html'