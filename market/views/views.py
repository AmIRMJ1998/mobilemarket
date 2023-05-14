from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q
# get models
from market.models import User,Mobile,Slider,Comment,Factor
from blog.models import Post

# --------------------------------------------------------------------------------------------------------------------------------

# Create your views here
def index(request):
    slides = Slider.objects.all()
    offMobiles = Mobile.objects.filter(publish = True, inventory__gt = 0, discount__gt = 0).order_by('-id')[:15]
    latestMobiles = Mobile.objects.filter(publish = True, inventory__gt = 0).order_by('-id')[:15]

    mobiles = Mobile.objects.filter(publish = True, inventory__gt = 0)

    class Items:
        def __init__(self, thisMobile, thisPoint):
            self.mobile = thisMobile
            self.point = thisPoint

    ItemsList = []

    for item in mobiles:
        totalPoint = 0
        if item.points is not None:
            for point in item.points:
                totalPoint += float(point['productRate'])
            item = Items(item, totalPoint/len(item.points))
            ItemsList.append(item)


    def GetPoint(item):
        return int(item.point)
    
    ItemsList.sort(reverse = True, key = GetPoint)

    ItemsList = ItemsList[:15]
    
    context = {
        'Slides': slides,
        'OffMobiles': offMobiles,
        'LatestMobiles': latestMobiles,
        'MostRateMobiles': ItemsList,
    }
    return render(request, 'market/index.html', context)

# def products(request):
#     return render(request, 'market/products.html')
def mobileFilter(request):
    response = {}
    try:
        available = request.POST['available']
    except MultiValueDictKeyError:
        available = ''
        
    try:
        brands = request.POST.getlist('brands[]')
    except MultiValueDictKeyError:
        brands = ''
        
    try:
        Max = request.POST['max']
    except MultiValueDictKeyError:
        Max = ''
        
    try:
        Min = request.POST['min']
    except MultiValueDictKeyError:
        Min = ''
        
    try:
        colors = request.POST.getlist('colors[]')
    except MultiValueDictKeyError:
        colors = ''
        
    try:
        simcard = request.POST['simcard']
    except MultiValueDictKeyError:
        simcard = ''
        
    try:
        internalMemory = request.POST.getlist('internalMemory[]')
    except MultiValueDictKeyError:
        internalMemory = ''
        
    try:
        ram = request.POST.getlist('ram[]')
    except MultiValueDictKeyError:
        ram = ''
        
    try:
        os = request.POST['os']
    except MultiValueDictKeyError:
        os = ''
        
    try:
        order = request.POST['order']
    except MultiValueDictKeyError:
        order = ''

    Mobiles = Mobile.objects.filter(publish = True)

    if available == '1':
        Mobiles = Mobiles.filter(inventory__gt = 0)
    #     for item in Mobiles:
    #         if item.inventory > 0 :
    #             mobiles.append(item)
    # else:
    #     for item in Mobiles:
    #         mobiles.append(item)
    
    if len(brands) != 0:
        Mobiles = Mobiles.filter(brand__in = brands)
        # for brand in brands:
        #     for item in mobiles:
        #         if item.brand == brand:
        #             mobiles.append(item)

    mobileList = list(Mobiles)
    removes = []
    if len(colors) != 0:
        for item in mobileList:
            find = False
            for single_color in colors:
                if item.colors is not None:
                    for color, _ in item.colors[0].items():
                        if single_color == color:
                            find = True
                else:
                    removes.append(item)
            if find == False:
                removes.append(item)

    for item in removes:
        mobileList.remove(item)

    removes = []
    if simcard == '1':
        for item in mobileList:
            for key, value in item.technical_details[1].items():
                if key == 'طراحی':
                    for k, v in value.items():
                        if (k == 'تعداد سیمکارت' or k == 'تعداد سیم کارت') and (v == 'دو سیم کارت' or v == 'دو سیمکارت'):
                            removes.append(item)
                            
    elif simcard == '2':
        for item in mobileList:
            for key, value in item.technical_details[1].items():
                if key == 'طراحی':
                    for k, v in value.items():
                        if (k == 'تعداد سیمکارت' or k == 'تعداد سیم کارت') and (v == 'یک سیم کارت' or v == 'یک سیمکارت' or v == 'تک سیمکارت' or v == 'تک سیم کارت'):
                            removes.append(item)
    
    for item in removes:
        mobileList.remove(item)

    removes = []
    if len(internalMemory) != 0:
        for item in mobileList:
            find = False
            for key, value in item.technical_details[3].items():
                if key == 'حافظه':
                    for k, v in value.items():
                        for imem in internalMemory:
                            if k == 'حافظه داخلی' and v == imem:
                                find = True
                    if find == False:
                        removes.append(item)
    for item in removes:
        mobileList.remove(item)

    removes = []
    if len(ram) != 0:
        for item in mobileList:
            find = False
            for key, value in item.technical_details[3].items():
                if key == 'حافظه':
                    for k, v in value.items():
                        for imem in ram:
                            if k == 'مقدار RAM' and v == imem:
                                find = True
                    if find == False:        
                        removes.append(item)

    for item in removes:
        mobileList.remove(item)


    if simcard == '1':
        for item in mobileList:
            for key, value in item.technical_details[1].items():
                if key == 'طراحی':
                    for k, v in value.items():
                        if (k == 'تعداد سیمکارت' or k == 'تعداد سیم کارت') and (v == 'دو سیم کارت' or v == 'دو سیمکارت'):
                            removes.append(item)
                            
    elif simcard == '2':
        for item in mobileList:
            for key, value in item.technical_details[1].items():
                if key == 'طراحی':
                    for k, v in value.items():
                        if (k == 'تعداد سیمکارت' or k == 'تعداد سیم کارت') and (v == 'یک سیم کارت' or v == 'یک سیمکارت' or v == 'تک سیمکارت' or v == 'تک سیم کارت'):
                            removes.append(item)
    removes = []
    if os == '1':
        for item in mobileList:
            for key, value in item.technical_details[8].items():
                if key == 'امکانات نرم افزاری':
                    for k, v in value.items():
                        if k == 'سیستم عامل' and (v == 'ios' or v == 'IOS'):
                            removes.append(item)

    if os == '2':
        for item in mobileList:
            for key, value in item.technical_details[8].items():
                if key == 'امکانات نرم افزاری':
                    for k, v in value.items():
                        if k == 'سیستم عامل' and (v == 'Android' or v == 'android' or v == 'اندروید'):
                            removes.append(item)
    

    for item in removes:
        mobileList.remove(item)

    removes = []
    for item in mobileList:
        if item.price > Max or item.price < Min:
            removes.append(item)

    for item in removes:
        mobileList.remove(item)

        # def __init__(self, thisMobile, thisPoint, thisPrice, thisDate):
    class Items:
        def __init__(self, thisMobile, thisPoint, thisPrice, thisDate):
            self.mobile = thisMobile
            self.point = thisPoint
            self.price = thisPrice
            self.date = thisDate

    ItemsList = []

    for item in mobileList:
        totalPoint = 0
        if item.points is not None:
            for point in item.points:
                totalPoint += float(point['productRate'])
            itemPoint = totalPoint/len(item.points)
        else:
            itemPoint = 0.0
        itemPrice = item.price
        itemDate = item.datecreate

        item = Items(item, itemPoint, itemPrice, itemDate)
        ItemsList.append(item)

                
                
        #     item = Items(item, totalPoint/len(item.points))
        #     ItemsList.append(item)
        # else:
        #     item = Items(item, 0.0)
        #     ItemsList.append(item)


    def GetPoint(item):
        return int(item.point)

    def GetPrice(item):
        return int(item.price)

    def GetDate(item):
        return item.date
    
    if order == 'favorite':
        ItemsList.sort(reverse = True, key = GetPoint)
    elif order == 'mostexpensive':
        ItemsList.sort(reverse = True, key = GetPrice)
    elif order == 'cheapest':
        ItemsList.sort(key = GetPrice)
    elif order == 'newest':
        ItemsList.sort(reverse = True, key = GetDate)

    # print(ItemsList)

    sortedMobileList = []
    for item in ItemsList:
        print(item.mobile)
        print(item.point)
        sortedMobileList.append(item.mobile)
    print(sortedMobileList)

    mobiles = []
    for item in sortedMobileList:
        mobile = {}
        mobile['image'] = item.index_image.url
        mobile['title'] = item.title
        mobile['slug'] = item.slug
        mobile['point'] = item.points
        mobile['discount'] = item.discount
        mobile['price'] = item.price
        mobile['inventory'] = item.inventory
        mobiles.append(mobile)
        # mobiles.append(model_to_dict(item))

    response['status'] = True
    response['mobiles'] = mobiles
    # if Max != '' or Min != '':
    #     Mobiles = Mobiles.filter(price__gt = Min, price__lt = Max)
        # for item in mobiles:
        #     if item.price > Min and item.price < Max:
        #         mobiles.append(item)
    return JsonResponse(response)

def mobile(request, inputBrand = ''):
    if request.method == 'POST':
        try:
            words = request.POST["search"]
            words = words.split(' ')
            words = list(filter(lambda i: i!='', words))
            search_words = []
            for word in words:
                search_word = list(map(lambda x: x + '\s*', word.replace(' ','')[:-1]))
                search_word = ''.join(search_word) + word[-1]
                search_words.append(search_word)
            search_word = r'.*'.join(search_words)
        except:
            word = False

        mobiles = Mobile.objects.filter(Q(title__regex = search_word) | Q(slug__regex = search_word) | Q(brand__regex = search_word), publish = True )

        mobilePaginator = Paginator (mobiles, 20)
        page = request.GET.get('page')
        mobiles = mobilePaginator.get_page(page)

        context = {
            'Mobiles': mobiles
        }
        return render(request, 'market/products-mobile.html', context)

    else:

        if inputBrand == '':
            Mobiles = Mobile.objects.filter(publish = True)
        elif inputBrand == 'samsung':
            Mobiles = Mobile.objects.filter(publish = True, brand = 'سامسونگ')
        elif inputBrand == 'sony':
            Mobiles = Mobile.objects.filter(publish = True, brand = 'سونی')
        elif inputBrand == 'lg':
            Mobiles = Mobile.objects.filter(publish = True, brand = 'ال جی')
        elif inputBrand == 'huawei':
            Mobiles = Mobile.objects.filter(publish = True, brand = 'هواوی')

        class Items:
            def __init__(self, thisMobile, thisPoint):
                self.mobile = thisMobile
                self.point = thisPoint
        if len(Mobiles) != 0:
            ItemsList = []

            for item in Mobiles:
                totalPoint = 0
                if item.points is not None:
                    for point in item.points:
                        totalPoint += float(point['productRate'])
                    item = Items(item, totalPoint/len(item.points))
                    ItemsList.append(item)
                else:
                    item = Items(item, 0.0)
                    ItemsList.append(item)


            def GetPoint(item):
                return int(item.point)
            
            ItemsList.sort(reverse = True, key = GetPoint)
            # print(ItemsList)

            sortedMobileList = []
            for item in ItemsList:
                print(item.mobile)
                print(item.point)
                sortedMobileList.append(item.mobile)
            print(sortedMobileList)

            MobilesBrands = []
            for item in Mobiles:
                if MobilesBrands is None:
                    MobilesBrands.append(item.brand)
                else:
                    if item.brand not in MobilesBrands:
                        MobilesBrands.append(item.brand)

            priceList = []
            for item in Mobiles:
                priceList.append(item.price)
            
            minPrice = min(priceList)
            maxPrice = max(priceList)

            yas =''
            MobilesColors = []
            for item in Mobiles:
                find = False
                if item.colors is not None:
                    for key, value in item.colors[0].items():
                        if len(MobilesColors) != 0:
                            for ky, _ in MobilesColors[0].items():
                                if key == ky:
                                    find = True
                        if find == False:        
                            for k, _ in value.items():
                                if key != yas:
                                    yas = key
                                    MobilesColors.append({key:k})


            MobileMemories = []
            for item in Mobiles:
                for a in item.technical_details:
                    for key, value in a.items():
                        if key == 'حافظه':
                            for k, v in value.items():
                                if k == 'حافظه داخلی':
                                    if v not in MobileMemories:
                                        MobileMemories.append(v)
                                        
            MobileRamMemories = []
            for item in Mobiles:
                for a in item.technical_details:
                    for key, value in a.items():
                        if key == 'حافظه':
                            for k, v in value.items():
                                if k == 'مقدار RAM':
                                    if v not in MobileRamMemories:
                                        MobileRamMemories.append(v)

            mobilePaginator = Paginator (sortedMobileList, 20)
            page = request.GET.get('page')
            sortedMobileList = mobilePaginator.get_page(page)

            context = {
                'Mobiles': sortedMobileList,
                'MobileBrands': MobilesBrands,
                'MobilesColors': MobilesColors,
                'MobileMemories': MobileMemories,
                'MobileRamMemories': MobileRamMemories,
                'minPrice': minPrice,
                'maxPrice': maxPrice,
                'inputBrand': inputBrand,
            }
        else:
            context = {
                'Empty': 'Empty',
            }
        return render(request, 'market/products-mobile.html', context)

# def tablet(request):
#     return render(request, 'market/products-tablet.html')

def product(request, Slug):
    thisMobile = Mobile.objects.get(slug = Slug)
    print(thisMobile.gallery.all())
    if request.user.is_authenticated:
        favorite = False
        favorites = request.user.favorite_list
        if favorites is not None:
            for item in favorites:
                if item == thisMobile.id:
                    favorite = True
    else:
        favorite = False

    commentList = {}
    if thisMobile.comments is not None:
        for item in thisMobile.comments:
            replies = []
            relativecomment = Comment.objects.get(id = item)
            if relativecomment.replay is not None:
                for item in relativecomment.replay:
                    reply = Comment.objects.get(id = item)
                    replies.append(reply)
            commentList[relativecomment] = replies

    context = {
        'mobile': thisMobile,
        'favorite': favorite,
        'commentList': commentList
    }

    return render(request, 'market/product.html', context)

@login_required(login_url="login")
def rate(request):
    res = {}
    if request.user.is_authenticated:
        try:
            if request.method == 'POST':
                try:
                    ProductRate = request.POST["productRate"]
                except MultiValueDictKeyError:
                    ProductRate = ''

                try:
                    mobileID = request.POST["mobileID"]
                except MultiValueDictKeyError:
                    mobileID = ''

                try:
                    thisMobile = Mobile.objects.get(id = mobileID)
                    userID = request.user.id
                    thisMobile.product_rate_set(userID = userID, productRate = ProductRate)

                    res['status'] = True
                    res['message'] = ProductRate
                    
                    return JsonResponse(res)
                except Exception as e:
                    print (str(e))
                    res['status'] = False
                    res['error'] = str(e)

                    return JsonResponse(res)
                


        except Exception as e:
            print (str(e))
            res['status'] = False
            res['error'] = str(e)
            return JsonResponse(res)
    else:
        return redirect("login")

@login_required(login_url="login")
def createComment(request):
    res = {}

    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                mobileID = request.POST["mobileID"]
            except MultiValueDictKeyError:
                mobileID = ''

            try:
                commentText = request.POST["commentText"]
            except MultiValueDictKeyError:
                commentText = ''

            user = request.user

            newComment = Comment()
            newComment.FK_User = user
            newComment.description = commentText
            newComment.save()

            thisMobile = Mobile.objects.get(id = mobileID)

            try:
                if thisMobile.comments is None:
                    thisMobile.comments = [newComment.id,]
                    thisMobile.save()
                    res['status'] = True
                    return JsonResponse(res)
                else:
                    newCommentID = int(newComment.id)
                    thisMobile.comments.append(newCommentID,)
                    thisMobile.save()
                    res['status'] = True
                    return JsonResponse(res)
            except Exception as e:
                print (e)
                res['error'] = str(e)
                res['status'] = False
                return JsonResponse(res)
    else:
        return redirect("login")

@login_required(login_url="login")
def likeComment(request):
    res = {}
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                commentID = request.POST["commentID"]
            except MultiValueDictKeyError:
                commentID = ''

            userID = int(request.user.id)
            thisComment = Comment.objects.get(id = commentID)
            remove = 0

            try:
                if thisComment.likes is not None:
                    for item in thisComment.likes:
                        if item == userID:
                            thisComment.likes.remove(userID)
                            thisComment.save()
                            res['likeCount'] = thisComment.like_count()
                            res['remove'] = 1
                            res['status'] = True
                            return JsonResponse(res)
                else:
                    thisComment.likes = [userID,]
                    thisComment.save()
                    res['likeCount'] = thisComment.like_count()
                    res['remove'] = 0
                    res['status'] = True
                    return JsonResponse(res)
                if remove != 1:
                    thisComment.likes.append(userID)
                    thisComment.save()
                    res['likeCount'] = thisComment.like_count()
                    res['remove'] = 0
                    res['status'] = True
                    return JsonResponse(res)
            except Exception as e:
                res['error'] = str(e)
                res['status'] = False
                return JsonResponse(res)
    else:
        res['error'] = 'login'
        res['status'] = False
        return JsonResponse(res)

@login_required(login_url="login")
def replyComment(request):
    res = {}

    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                commentID = request.POST["commentID"]
            except MultiValueDictKeyError:
                commentID = ''

            try:
                commentText = request.POST["commentText"]
            except MultiValueDictKeyError:
                commentText = ''

            user = request.user
            thisComment = Comment.objects.get(id = commentID)

            try:
                newComment = Comment()
                newComment.FK_User = user
                newComment.description = commentText
                newComment.save()
            except Exception as e:
                res['error'] = str(e)
                res['status'] = False
                return JsonResponse(res)

            try:
                if thisComment.replay is None:
                    thisComment.replay = [newComment.id]
                    thisComment.save()
                    res['status'] = True
                    return JsonResponse(res)
                else:
                    thisComment.replay.append(newComment.id)
                    thisComment.save()
                    res['status'] = True
                    return JsonResponse(res)
            except Exception as e:
                res['error'] = str(e)
                res['status'] = False
                return JsonResponse(res)

@login_required(login_url="login")
def card(request):
    if Factor.objects.filter(FK_User = request.user, payment_status = False).exists():
        factor = Factor.objects.get(FK_User = request.user, payment_status = False)

        totalFactorPrice = factor.get_total_price()
        for item in factor.items['items']:
            mobileID = item['id']
            thisMobile = Mobile.objects.get(id = mobileID)
            item['id'] = thisMobile

        factorItems = factor.items['items']
    else:
        factorItems = []
        totalFactorPrice = ''

    context = {
        'factorItems': factorItems,
        'totalFactorPrice': totalFactorPrice
    }

    return render(request, 'market/card.html', context)


def register(request):
    return render(request, 'market/register-login/register.html')

def registerRequest(request):
    response_data = {}
        # get data
    firstname = request.POST.get("firstname")
    lastname = request.POST.get("lastname")
    username = request.POST.get("username")
    # content = request.POST.get("content")
    password = request.POST.get("password")
    email = request.POST.get("email")
    nationalcode = request.POST.get("nationalcode")
    repeat_password = request.POST.get("repeat_password")

    try:
        birthday = request.POST.get('birthday')
    except MultiValueDictKeyError:
        birthday = ''

    try:
        mobile = request.POST.get('mobile')
    except MultiValueDictKeyError:
        mobile = ''

    try:
        phone = request.POST.get('phone')
    except MultiValueDictKeyError:
        phone = ''

    try:
        citypercode = request.POST.get('citypercode')
    except MultiValueDictKeyError:
        citypercode = ''

    try:
        state = request.POST.get('state')
    except MultiValueDictKeyError:
        state = ''

    try:
        city = request.POST.get('city')
    except MultiValueDictKeyError:
        city = ''

    try:
        address = request.POST.get('address')
    except MultiValueDictKeyError:
        address = ''

    try:
        zipcode = request.POST.get('zipcode')
    except MultiValueDictKeyError:
        zipcode = ''

    
    # uvc = request.POST.get("verification_code") # user verification code
    # check user verification code
    # if Validation.objects.filter(value = content, valid_code = uvc, status = False).exists():
        # check password and repeat password
    if password == repeat_password:
            # change user verification code status 
            # this_uvc = Validation.objects.get(value = content, valid_code = uvc, status = False)
            # this_uvc.status = True
            # this_uvc.save()
            # create new user
            
        try:
            this_user = User.objects.create_user(username = username, password = password, email = email, nationalcode = nationalcode)
            # set other data
            this_user.first_name = firstname
            this_user.last_name = lastname
            this_user.mobile = mobile
            # this_user.email = email
            # this_user.nationalcode = nationalcode
            this_user.user_address(this_state = state, this_city = city, this_zipcode = zipcode, this_address = address)
            this_user.citypercode = citypercode
            this_user.phone = phone
            this_user.birthday = birthday
            this_user.save()
            
            # if this_uvc.value_type:
            #     this_user.mobile = content
            # else:
            #     this_user.email = content
            # this_user.save()
            # login user
            login(request, this_user)

            response_data['status'] = True
            response_data['message'] = 'ثبت نام با موفقیت انجام شد'
            return JsonResponse(response_data)
        except Exception as e:
            response_data['status'] = False
            response_data['message'] = str(e)
            return JsonResponse(response_data)

    else:
        response_data['status'] = False
        response_data['message'] = 'رمز عبور و تکرار آن بایستی با یکدیگر تطابق داشته باشند'
        return JsonResponse(response_data)
        # else:
        #     response_data['status'] = True
        #     response_data['message'] = '403'
        #     return JsonResponse(response_data)

def loginPage(request):
    return render(request, 'market/register-login/login.html')

@login_required(login_url="login")
def dashboard(request):
    return render(request, 'account/dashboard.html')

@login_required(login_url="login")
def orders(request):
    factors = Factor.objects.filter(FK_User = request.user)

    for factor in factors:
        for item in factor.items['items']:
            mobileID = item['id']
            thisMobile = Mobile.objects.get(id = mobileID)
            item['id'] = thisMobile

    context = {
        'factors': factors
    }

    return render(request, 'account/orders.html', context)

@login_required(login_url="login")
def order(request, id):
    thisfactor = Factor.objects.get(id = id)

    for item in thisfactor.items['items']:
        mobileID = item['id']
        thisMobile = Mobile.objects.get(id = mobileID)
        item['id'] = thisMobile

    context = {
        'factor': thisfactor,
    }

    return render(request, 'account/order.html', context)

@login_required(login_url="login")
def information(request):
    return render(request, 'account/information.html')

@login_required(login_url="login")
def changeInformation(request):
    res = {
        'has_message': False,
        'has_error': False
    }

    if request.user.is_authenticated:
        try:
            if request.method == 'POST':
                try:
                    FirstName = request.POST["firstname"]
                except MultiValueDictKeyError:
                    FirstName = ''

                try:
                    LastName = request.POST["lastname"]
                except MultiValueDictKeyError:
                    LastName = ''

                try:
                    Email = request.POST["email"]
                except MultiValueDictKeyError:
                    Email = ''

                # try:
                #     birthday_day = request.POST["birthday-day"]
                # except MultiValueDictKeyError:
                #     birthday_day = ''

                # try:
                #     birthday_month = request.POST["birthday-month"]
                # except MultiValueDictKeyError:
                #     birthday_month = ''

                # try:
                #     birthday_year = request.POST["birthday-year"]
                # except MultiValueDictKeyError:
                #     birthday_year = ''

                try:
                    birthday = request.POST["birthday"]
                except MultiValueDictKeyError:
                    birthday = ''

                try:
                    MobileNumber = request.POST["mobilenumber"]
                except MultiValueDictKeyError:
                    MobileNumber = ''

                try:
                    PhoneNumber = request.POST["phonenumber"]
                except MultiValueDictKeyError:
                    PhoneNumber = ''

                try:
                    PrePhoneNumber = request.POST["prephonenumber"]
                except MultiValueDictKeyError:
                    PrePhoneNumber = ''

                try:
                    State = request.POST["state"]
                except MultiValueDictKeyError:
                    State = ''

                try:
                    City = request.POST["city"]
                except MultiValueDictKeyError:
                    City = ''

                try:
                    Address = request.POST["address"]
                except MultiValueDictKeyError:
                    Address = ''

                try:
                    PostalCode = request.POST["postalcode"]
                except MultiValueDictKeyError:
                    PostalCode = ''

                if (FirstName != '') and (LastName != '') and (Email != '') and (MobileNumber != ''):
                    this_user = request.user

                    # BirthDay = birthday_year + '-' + birthday_month + '-' + birthday_day

                    this_user.first_name = FirstName
                    this_user.last_name = LastName
                    this_user.email = Email
                    this_user.birthday = birthday
                    this_user.mobile = MobileNumber
                    this_user.phone = PhoneNumber
                    this_user.citypercode = PrePhoneNumber
                    this_user.user_address(this_state = State, this_city = City, this_zipcode = PostalCode, this_address = Address)


                    res['has_message'] = True
                    res['message'] = 'مشخصات شما با موفقیت تغییر یافت'
                    # return redirect('information')
                    return JsonResponse(res)

                else:
                    res['has_error'] = True
                    res['error'] = 'مشخصات ضروری نمیتواند خالی باشد!'
                    # return redirect('information')
                    return JsonResponse(res)

        except Exception as e:
            res['has_error'] = True
            res['error'] = str(e)
            # return redirect('information')
            return JsonResponse(res)
    else:
        return redirect("login")

@login_required(login_url="login")
def favorites(request):
    thisUser = request.user
    favorites = thisUser.favorite_list
    mobile = []
    for item in favorites:
        mobile.append(Mobile.objects.get(id = item))

    context = {
        'favoritemobiles': mobile
    }

    return render(request, 'account/favorites.html', context)

@login_required(login_url="login")
def addtofavorite(request):
    res = {}

    if request.user.is_authenticated:
        try:
            if request.method == 'POST':
                try:
                    mobileID = request.POST["mobileID"]
                except MultiValueDictKeyError:
                    mobileID = ''

                print (mobileID)
                thisUser = request.user
                remove = 0
                print (thisUser)

                if thisUser.favorite_list is not None:
                    for favorite in thisUser.favorite_list:
                        favorite = int(favorite)
                        mobileID = int(mobileID)
                        if favorite == mobileID:
                            remove = 1
                            thisUser.favorite_list.remove(favorite)
                            thisUser.save()
                            res['remove'] = 1
                            res['status'] = True

                if remove != 1:
                    try:
                        thisUser.favorite_list.append(mobileID)
                        thisUser.save()
                        res['remove'] = 0
                        res['status'] = True
                    except Exception as e:
                        res['error'] = str(e)
                        res['status'] = False

            return JsonResponse(res)
        except Exception as e:
            res['error'] = str(e)
            res['status'] = False
            return JsonResponse(res)

    else:
        return redirect("login")

@login_required(login_url="login")
def messages(request):
    userMessages = []
    allmessages = Message.objects.all()
    for message in allmessages:
        for item in message.users:
            if item["userID"] == request.user.id:
                userMessages.append(message)

    context = {
        'messages': userMessages
    }
                
    return render(request, 'account/messages.html', context)

@login_required(login_url="login")
def message(request, id):
    message = Message.objects.get(id = id)
    context = {
        'message': message
    }
    return render(request, 'account/message.html', context)

@login_required(login_url="login")
def changeMessageStatus(request):
    res = {}

    if request.user.is_authenticated:
        if request.POST.get('action') == 'post':
            messageID = request.POST["id"]
            message = Message.objects.get(id = messageID)
            userID = request.user.id

            for item in message.users:
                print (item['userID'])
                if item['userID'] == userID:
                    item['seen'] = "1"
                    message.save()
                    res['status'] = True
    return JsonResponse(res)


# def comments(request):
#     return render(request, 'account/comments.html')

def compare(request):

    brands = []

    mobiles = Mobile.objects.all()

    for mobile in mobiles:
        
        if len(brands) == 0:
            brands.append(mobile.brand)
        else: 
            find = False
            brandslen = len(brands)
            iteration = 0
            for brand in brands:
                iteration += 1
                if brand == mobile.brand:
                    find = True
                elif find == False and iteration == brandslen:
                    brands.append(mobile.brand)

    context = {
        'brands': brands
    }
    
    return render(request, 'market/compare.html', context)

def findMobileByBrand(request):
    res = {}

    if request.method == 'POST':
        try:
            brand = request.POST['brand']
        except MultiValueDictKeyError:
            brand = ''

        try:
            thisBrandMobiles = Mobile.objects.filter(brand = brand)
            if thisBrandMobiles is None:
                res['error'] = 'محصولی با این برند ثبت نشده است!'
                res['status'] = False
                return JsonResponse(res)
            thisBrandMobilesList = []
            for mobile in thisBrandMobiles:
                thisBrandMobilesList.append({mobile.id: mobile.title})
            res['thisBrandMobiles'] = thisBrandMobilesList
            res['status'] = True
            return JsonResponse(res)

        except Exception as e:
            res['error'] = str(e)
            res['status'] = False
            return JsonResponse(res)

def addToCompare(request):
    res = {}

    if request.method == 'POST':

        try:
            mobileID = request.POST['mobileID']
        except MultiValueDictKeyError:
            mobileID = ''

        try:
            mobile = Mobile.objects.get(id = mobileID)
            if mobile is not None:
                res['id'] = mobile.id
                res['title'] = mobile.title
                res['slug'] = mobile.slug
                res['image'] = mobile.index_image.url
                res['status']= True
                return JsonResponse(res)
            else:
                res['error']= 'این محصول وجود ندارد!'
                res['status']= False
                return JsonResponse(res)
        except Exception as e:
            res['error']= str(e)
            res['status']= False
            return JsonResponse(res)

def doCompare(request):
    res = {}
    finalList1 = []
    finalList2 = []

    if request.method == 'POST':
        try:
            mobid1 = request.POST['mobileid1']
        except MultiValueDictKeyError:
            mobid1 = request.POST['mobileid1']

        try:
            mobid2 = request.POST['mobileid2']
        except MultiValueDictKeyError:
            mobid2 = request.POST['mobileid2']

        mobile1 = Mobile.objects.get(id = mobid1)
        mobile2 = Mobile.objects.get(id = mobid2)
        res['title1'] = mobile1.title
        res['title2'] = mobile2.title
        res['slug1'] = mobile1.slug
        res['slug2'] = mobile2.slug
        res['image1'] = mobile1.index_image.url
        res['image2'] = mobile2.index_image.url
        res['price1'] = mobile1.price
        res['price2'] = mobile2.price
        res['inventory1'] = mobile1.inventory
        res['inventory2'] = mobile2.inventory

        for item in mobile1.technical_details:
            for key, value in item.items():
                jsonvar1 = {key: {}}
                arraym = []
                for x, y in value.items():
                    arraym.append({x: [y]})
                jsonvar1[key] = arraym
                finalList1.append(jsonvar1)

        for item in mobile2.technical_details:
            for key, value in item.items():
                jsonvar1 = {key: {}}
                arraym = []
                for x, y in value.items():
                    arraym.append({x: [y]})
                jsonvar1[key] = arraym
                finalList2.append(jsonvar1)

        for tarikhtarahijs1 in finalList1:
            found = False
            for tarikhtarahi1, miladishamsilist1 in tarikhtarahijs1.items():
                iteration = 0
                finalList2len = len(finalList2)
                for tarikhtarahijs2 in finalList2:
                    iteration += 1
                    for tarikhtarahi2, miladishamsilist2 in tarikhtarahijs2.items():
                        if tarikhtarahi2 == tarikhtarahi1:
                            found = True
                            for miladishamsijs1 in miladishamsilist1:
                                find = False
                                for miladishamsi1, shahrivarnovemberlist1 in miladishamsijs1.items():
                                    iterate = 0
                                    miladishamsilist2len = len(miladishamsilist2)
                                    for miladishamsijs2 in miladishamsilist2:
                                        iterate += 1
                                        for miladishamsi2, shahrivarnovemberlist2 in miladishamsijs2.items():
                                            if miladishamsi1 == miladishamsi2:
                                                for shahrivarnovember2 in shahrivarnovemberlist2:
                                                    shahrivarnovemberlist1.append(shahrivarnovember2)
                                                    find = True
                                            elif iterate == miladishamsilist2len and find == False:
                                                shahrivarnovemberlist1.append("------")
                        elif iteration == finalList2len and found == False:
                            for miladishamsijs1 in miladishamsilist1:
                                for miladishamsi1, shahrivarnovemberlist1 in miladishamsijs1.items():
                                    shahrivarnovemberlist1.append("------")

        for tarikhtarahijs2 in finalList2:
            sfound = False
            for tarikhtarahi2, miladishamsilist2 in tarikhtarahijs2.items():
                siteration = 0
                finalList1len = len(finalList1)
                for tarikhtarahijs1 in finalList1:
                    siteration += 1
                    for tarikhtarahi1, miladishamsilist1 in tarikhtarahijs1.items():
                        if tarikhtarahi2 == tarikhtarahi1:
                            sfound = True
                            for miladishamsijs2 in miladishamsilist2:
                                sfind = False
                                for miladishamsi2, shahrivarnovemberlist2 in miladishamsijs2.items():
                                    siterate = 0
                                    miladishamsilist1len = len(miladishamsilist1)
                                    for miladishamsijs1 in miladishamsilist1:
                                        siterate += 1
                                        for miladishamsi1, shahrivarnovemberlist1 in miladishamsijs1.items():
                                            if miladishamsi2 == miladishamsi1:
                                                sfind = True
                                            elif siterate == miladishamsilist1len and sfind == False:
                                                shahrivarnovemberlist2.insert(0, '------')
                                                miladishamsilist1.append({miladishamsi2: shahrivarnovemberlist2})
                        elif siteration == finalList1len and sfound == False:
                            for miladishamsijs2 in miladishamsilist2:
                                for miladishamsi2, shahrivarnovemberlist2 in miladishamsijs2.items():
                                    shahrivarnovemberlist2.insert(0, '------')
                            finalList1.append({tarikhtarahi2: miladishamsilist2})
        res['compareList'] = finalList1
        return JsonResponse(res)


def contactUs(request):
    return render(request, 'market/contact-us.html')

def rules(request):
    return render(request, 'market/rules.html')

def loginRequest(request):
    resp = {}

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('market:index')
        else:
            resp['error'] = 'نام کاربری یا رمز عبور اشتباه است!'
            return render(request, 'market/register-login/login.html', resp)

    else:
        resp['error'] = 'خطا! صفحه را رفرش کرده مجددا سعی نمائید'
        return render(request, 'market/register-login/login.html', resp)

def logoutRequest(request):
    logout(request)
    return HttpResponseRedirect(reverse('market:index'))

def lastComments(request):
    res = {}
    if request.method == 'POST':
        comments = Comment.objects.order_by('-id')[:3]

        commentsList = []
        for comment in comments:
            commentsJS = {}
            commentsJS[comment.FK_User.username] = comment.description
            commentsList.append(commentsJS)
        res['comments'] = commentsList
        return JsonResponse(res)


def lastPosts(request):
    res = {}
    if request.method == 'POST':
        postsList = []
        for item in Post.objects.order_by('-publishdate')[:6]:
            postsJS = {}
            # url = str(item.get_url)
            url = item.get_url()
            postsJS[url] = item.get_title()
            postsList.append(postsJS)
        res['posts'] = postsList
        return JsonResponse(res)