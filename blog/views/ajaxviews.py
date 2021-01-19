from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
import datetime
# get model
from market.models import Comment
from blog.models import Post

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# add new comment
@login_required(login_url="login")
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
            response_data['error'] = 'کامنت تکراری'
            return JsonResponse(response_data)
        else:
            # create new object
            this_comment = Comment.objects.create(description = this_description, FK_User = request.user)
            this_post = Post.objects.get(slug = this_slug)
            # add comment
            this_post.comments.append(this_comment.id)

            response_data['status'] = True
            return JsonResponse(response_data)
    except Exception as e:
        response_data['status'] = False
        response_data['error'] = str(e)
        return JsonResponse(response_data)

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

# like or dislike comment
@login_required(login_url="login")
def like_or_dislike_comment(request):
    response_data = {}
    try:
        # get data
        this_id = request.POST.get("id")
        # get this comment
        this_comment = Comment.objects.get(id = this_id, FK_User = request.user)
        # check repete data
        if this_comment.likes is not None:
            if request.user.id in this_comment.likes:
                # dislike
                this_comment.likes.remove(request.user.id)
                this_comment.save()

                response_data['status'] = True
                response_data['remove'] = 1
                return JsonResponse(response_data)
            else:
                # like
                this_comment.likes.append(request.user.id)
                this_comment.save()

                response_data['status'] = True
                response_data['remove'] = 0
                return JsonResponse(response_data)
        else:
            this_comment.likes = [request.user.id]
            this_comment.save()
            
            response_data['status'] = True
            response_data['remove'] = 0
            return JsonResponse(response_data)

    except Exception as e:
        response_data['status'] = False
        response_data['error'] = str(e)
        return JsonResponse(response_data)


# add point in post
@login_required(login_url="login")
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
# def set_session(request):
#     response_data = {}
#     try:
#         this_path = request.POST['this_path']
#         # get path other than non-account path 
#         if not ((this_path == '/signin/') or (this_path == '/signup/') or (this_path == '/forgotpassword/')):
#             request.session['next'] = this_path
#         response_data['status'] = True
#         return JsonResponse(response_data)
#     except Exception as e:
#         response_data['status'] = False
#         response_data['message'] = str(e)
#         return JsonResponse(response_data)