from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils import timezone
import datetime
# get model
from market.models import Comment
from blog.models import Post

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# add new comment
def add_new_comment(request):
    response_data = {}
    try:
        # get data
        this_slug = request.POST.get("slug")
        this_description = request.POST.get("description")
        # check repete data
        if Comment.objects.filter(description = this_description, FK_User = request.user).exists():
            # duplicate data
            response_data['status'] = False
            return JsonResponse(response_data)
        else:
            # create new object
            this_comment = Comment.objects.create(description = this_description, FK_User = request.user)
            this_post = Post.objects.get(slug = this_slug)
            # add comment
            this_post.post_comments(this_comment.id)

            response_data['status'] = True
            return JsonResponse(response_data)
    except Exception as e:
        response_data['status'] = False
        response_data['message'] = str(e)
        return JsonResponse(response_data)


# like or dislike comment
def like_or_dislike_comment(request):
    response_data = {}
    try:
        # get data
        this_id = request.POST.get("id")
        # get this comment
        this_comment = Comment.objects.get(id = this_id, FK_User = request.user)
        # check repete data
        if request.user.id in this_comment.likes:
            # dislike
            this_comment.likes.remove(request.user.id)

            response_data['status'] = True
            return JsonResponse(response_data)
        else:
            # like
            this_comment.likes.append(request.user.id)

            response_data['status'] = True
            return JsonResponse(response_data)
    except Exception as e:
        response_data['status'] = False
        response_data['message'] = str(e)
        return JsonResponse(response_data)


# add point in post
def add_point_in_post(request):
    response_data = {}
    try:
        # get data
        this_id = request.POST.get("id")
        this_point = request.POST.get("point")
        # get this post
        this_post = Post.objects.get(id = this_id)
        # call post point functions
        this_post.post_points(request.user.id, this_point)

        response_data['status'] = True
        return JsonResponse(response_data)
    except Exception as e:
        response_data['status'] = False
        response_data['message'] = str(e)
        return JsonResponse(response_data)


# set session
def set_session(request):
    response_data = {}
    try:
        this_path = request.POST['this_path']
        # get path other than non-account path 
        if not ((this_path == '/signin/') or (this_path == '/signup/') or (this_path == '/forgotpassword/')):
            request.session['next'] = this_path
        response_data['status'] = True
        return JsonResponse(response_data)
    except Exception as e:
        response_data['status'] = False
        response_data['message'] = str(e)
        return JsonResponse(response_data)