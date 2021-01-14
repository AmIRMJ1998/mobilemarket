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
def add_new_comment(request, slug):
    response_data = {}
    try:
        # get data
        this_title = request.POST.get("title")
        this_description = request.POST.get("description")
        # check repete data
        if Comment.objects.filter(title = this_title, datecreate = this_description, FK_User = request.user).exists():
            # duplicate data
            response_data['status'] = False
            return JsonResponse(response_data)
        else:
            # create new object
            this_comment = Comment.objects.create(title = this_title, datecreate = this_description, FK_User = request.user)
            this_post = Post.objects.get(slug = slug)
            # add comment
            this_post.post_comments(this_comment.id)

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