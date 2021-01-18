from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q
from django.contrib.postgres.fields import ArrayField
import jdatetime
import threading

from market.models import Slider, Mobile, User, Message, Comment


# Create your views here
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

# def products(request):
#     return render(request, 'market/products.html')

def mobile(request):
    Mobiles = Mobile.objects.filter(publish = True)

    context = {
        'Mobiles': Mobiles
    }
    return render(request, 'market/products-mobile.html', context)

# def tablet(request):
#     return render(request, 'market/products-tablet.html')

def product(request, Slug):
    thisMobile = Mobile.objects.get(slug = Slug)
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


def card(request):
    return render(request, 'market/card.html')

def addToCard(request):
    res = {}

    if request.user.is_authenticated:
        if request.method == 'POST':
            return
    else:
        return redirect('login')

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

                if (FirstName != '') and (LastName != '') and (Email != ''):
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

def message(request, id):
    message = Message.objects.get(id = id)
    context = {
        'message': message
    }
    return render(request, 'account/message.html', context)
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


def comments(request):
    return render(request, 'account/comments.html')

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
