from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from market.models import Comment
from blog.models import Post

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def blogindex(request):
    # get new post
    post_list = Post.objects.all().order_by('-publishdate')

    class Items:
        def __init__(self, thisPost, thisPoint):
            self.post = thisPost
            self.point = thisPoint

    ItemsList = []

    for item in post_list:
        sum_points = 0.0
        for this_point in item.points['list']:
            sum_points += int(this_point['point'])
        sum_points =  sum_points / len(item.points['list'])

        item = Items(item, sum_points)
        ItemsList.append(item)

    def GetPoint(item):
        return int(item.point)
    
    ItemsList.sort(reverse = True, key = GetPoint)

    blogPaginator = Paginator (post_list, 7)
    page = request.GET.get('page')
    post_list = blogPaginator.get_page(page)

    content = {
        "PostList": post_list,
        "side_posts": ItemsList,
    }
    return render(request, 'blog/blog-index.html', content)

def blogPost(request, slug):
    # get this post
    this_post = get_object_or_404(Post, slug = slug, publish = True)

    commentList = {}
    if this_post.comments is not None:
        for item in this_post.comments:
            replies = []
            relativecomment = Comment.objects.get(id = item)
            if relativecomment.replay is not None:
                for item in relativecomment.replay:
                    reply = Comment.objects.get(id = item)
                    replies.append(reply)
            commentList[relativecomment] = replies
    
    # comments = Comment.objects.filter(id__in = this_post.comments)

    content = {
        "ThisPost": this_post,
        "Comments": commentList,
    }
    return render(request, 'blog/blog-post.html', content)