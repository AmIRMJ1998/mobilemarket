from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
import threading

from .models import Slider
from .models import Mobile
from .models import User

class GetUserInfo(threading.Thread):
    def run(self, request):
        this_user_profile = get_object_or_404(User, FK_User = request.user)
        result = {
            "user_profile": this_user_profile,
        }
        return result

def index(request):
    slides = Slider.objects.all()
    offMobiles = Mobile.objects.filter(publish = True, inventory__gt = 0, discount__gt = 0).order_by('-id')[:15]
    latestMobiles = Mobile.objects.filter(publish = True, inventory__gt = 0).order_by('-id')[:15]
    mostRateMobiles = Mobile.objects.filter(publish = True, inventory__gt = 0).order_by('-id')[:15]

    context = {
        'Slides': slides,
        'OffMobiles': offMobiles,
        'LatestMobiles': latestMobiles,
        'MostRateMobiles': mostRateMobiles,
    }
    return render(request, 'market/index.html', context)

def products(request):
    return render(request, 'market/products.html')

def mobile(request):
    return render(request, 'market/products-mobile.html')

def tablet(request):
    return render(request, 'market/products-tablet.html')

def product(request, slug):
    return render(request, 'market/product.html')

def card(request):
    return render(request, 'market/card.html')

def register(request):
    return render(request, 'market/register-login/register.html')

def loginPage(request):
    return render(request, 'market/register-login/login.html')

def dashboard(request):
    return render(request, 'account/dashboard.html')

def orders(request):
    return render(request, 'account/orders.html')

def order(request):
    return render(request, 'account/order.html')

@login_required(login_url="login")
def information(request):
    # this_user = GetUserInfo().run(request)
    # this_profile = this_user["user_profile"]
    this_profile = request.user
    
    context = {
            'User_Profile':this_profile,
    }

    return render(request, 'account/information.html', context)

def favorites(request):
    return render(request, 'account/favorites.html')

def messages(request):
    return render(request, 'account/messages.html')

def message(request):
    return render(request, 'account/message.html')

def comments(request):
    return render(request, 'account/comments.html')

def compare(request):
    return render(request, 'market/compare.html')

def contactUs(request):
    return render(request, 'market/contact-us.html')

def loginRequest(request):
    resp = {}

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            resp['error'] = 'نام کاربری یا رمز عبور اشتباه است!'
            return render(request, 'market/register-login/login.html', resp)

    else:
        resp['error'] = 'خطا! صفحه را رفرش کرده مجددا سعی نمائید'
        return render(request, 'market/register-login/login.html', resp)

def logoutRequest(request):
    logout(request)
    return HttpResponseRedirect(reverse(index))