from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils import timezone
import datetime
# get model
from market.models import Mobile, Factor, User

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# add new item in factor
def add_new_item_in_factor(request):
    response_data = {}
    try:
        # get data
        this_mobile_id = request.POST.get("id")
        this_color = request.POST.get("color")
        this_color_value = request.POST.get("color_value")
        # check repete data
        if Factor.objects.filter(FK_User = request.user, payment_status = False).exists():
            # add date
            this_factor = Factor.objects.get(FK_User = request.user, payment_status = False)
            this_mobile = Mobile.objects.get(id = this_mobile_id)
            this_factor.add_item(this_mobile, 1, this_color, this_color_value)

            response_data['status'] = True
            return JsonResponse(response_data)
        else:
            # create new object
            this_factor = Factor.objects.create(FK_User = request.user)
            this_mobile = Mobile.objects.get(id = this_mobile_id)
            this_factor.add_item(this_mobile, 1, this_color, this_color_value)

            response_data['status'] = True
            return JsonResponse(response_data)
    except Exception as e:
        response_data['status'] = False
        response_data['message'] = str(e)
        return JsonResponse(response_data)


# add singel item count
def add_singel_item_count(request):
    response_data = {}
    try:
        # get data
        this_mobile_id = request.POST.get("id")
        this_color = request.POST.get("color")
        # check repete data
        if Factor.objects.filter(FK_User = request.user, payment_status = False).exists():
            this_factor = Factor.objects.get(FK_User = request.user, payment_status = False)
            this_mobile = Mobile.objects.get(id = this_mobile_id)
            for item in this_factor.items:
                if (item.id == this_mobile.id) and (item.color == this_color) and (this_mobile.inventory > 0):
                    item.count += 1
                    item.total_price = this_mobile.get_total_price(item.count + 1)
                    this_factor.save()

                    response_data['status'] = True
                    return JsonResponse(response_data)
                else:
                    response_data['status'] = False
                    return JsonResponse(response_data)
        else:
            response_data['status'] = False
            return JsonResponse(response_data)
    except Exception as e:
        response_data['status'] = False
        response_data['message'] = str(e)
        return JsonResponse(response_data)


# remove singel item count
def remove_singel_item_count(request):
    response_data = {}
    try:
        # get data
        this_mobile_id = request.POST.get("id")
        this_color = request.POST.get("color")
        # check repete data
        if Factor.objects.filter(FK_User = request.user, payment_status = False).exists():
            this_factor = Factor.objects.get(FK_User = request.user, payment_status = False)
            this_mobile = Mobile.objects.get(id = this_mobile_id)
            for item in this_factor.items:
                if (item.id == this_mobile.id) and (item.color == this_color):
                    if item.count - 1 != 0:
                        item.count -= 1
                        item.total_price = this_mobile.get_total_price(item.count - 1)
                        this_factor.save()
                    else:
                        this_factor.items['items'].remove(item)
                        this_factor.save()

                    response_data['status'] = True
                    return JsonResponse(response_data)
                else:
                    response_data['status'] = False
                    return JsonResponse(response_data)
        else:
            response_data['status'] = False
            return JsonResponse(response_data)
    except Exception as e:
        response_data['status'] = False
        response_data['message'] = str(e)
        return JsonResponse(response_data)


# remove item in factor
def remove_item_in_factor(request):
    response_data = {}
    try:
        # get data
        this_mobile_id = request.POST.get("id")
        this_color = request.POST.get("color")
        # check repete data
        if Factor.objects.filter(FK_User = request.user, payment_status = False).exists():
            this_factor = Factor.objects.get(FK_User = request.user, payment_status = False)
            this_mobile = Mobile.objects.get(id = this_mobile_id)
            for item in this_factor.items:
                if (item.id == this_mobile.id) and (item.color == this_color):
                    this_factor.items['items'].remove(item)
                    this_factor.save()

                    response_data['status'] = True
                    return JsonResponse(response_data)
                else:
                    response_data['status'] = False
                    return JsonResponse(response_data)
        else:
            response_data['status'] = False
            return JsonResponse(response_data)
    except Exception as e:
        response_data['status'] = False
        response_data['message'] = str(e)
        return JsonResponse(response_data)


# add information in factor
def add_information_in_factor(request):
    response_data = {}
    try:
        # get data
        this_state = request.POST.get("state")
        this_city = request.POST.get("city")
        this_mobile = request.POST.get("mobile")
        this_phone = request.POST.get("phone")
        this_per_city_phone = request.POST.get("per_city_phone")
        this_address = request.POST.get("address")
        this_zipcode = request.POST.get("zipcode")
        # check data
        if Factor.objects.filter(FK_User = request.user, payment_status = False).exists():
            this_factor = Factor.objects.get(FK_User = request.user, payment_status = False)
            # add date
            this_factor.FK_User = request.user
            this_factor.add_address(this_state, this_city, this_zipcode, this_address, this_phone, this_per_city_phone, this_mobile)
            this_factor.save()

            response_data['status'] = True
            return JsonResponse(response_data)
        else:
            response_data['status'] = False
            return JsonResponse(response_data)
    except Exception as e:
        response_data['status'] = False
        response_data['message'] = str(e)
        return JsonResponse(response_data)


# check out factor
def set_session(request):
    response_data = {}
    try:
        # get data
        this_post_price = request.POST.get("post_price")
        # check data
        if Factor.objects.filter(FK_User = request.user, payment_status = False).exists():
            this_factor = Factor.objects.get(FK_User = request.user, payment_status = False)
            # add date
            this_factor.post_price = this_post_price
            this_factor.total_price = this_factor.grt_total_price() + int(this_post_price)
            this_factor.payment_status = True
            this_factor.orderdate = timezone.now()
            this_factor.status = 1
            this_factor.save()

            response_data['status'] = True
            return JsonResponse(response_data)
        else:
            response_data['status'] = False
            return JsonResponse(response_data)
    except Exception as e:
        response_data['status'] = False
        response_data['message'] = str(e)
        return JsonResponse(response_data)