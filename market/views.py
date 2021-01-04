from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'market/index.html')

def products(request):
    return render(request, 'market/products.html')

def mobile(request):
    return render(request, 'market/products-mobile.html')

def tablet(request):
    return render(request, 'market/products-tablet.html')

def product(request):
    return render(request, 'market/product.html')

def card(request):
    return render(request, 'market/card.html')

def register(request):
    return render(request, 'market/register-login/register.html')

def login(request):
    return render(request, 'market/register-login/login.html')

def dashboard(request):
    return render(request, 'account/dashboard.html')

def orders(request):
    return render(request, 'account/orders.html')

def order(request):
    return render(request, 'account/order.html')

def information(request):
    return render(request, 'account/information.html')

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