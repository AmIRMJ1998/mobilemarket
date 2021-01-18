from django.shortcuts import get_object_or_404
from django.shortcuts import render
from market.models import Comment
from blog.models import Post

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def blogindex(request):
    # get new post
    post_list = Post.objects.all().order_by('-publishdate')

    content = {
        "PostList": post_list,
    }
    return render(request, 'blog/blog-index.html', content)

def blogPost(request, slug):
    # get this post
    this_post = get_object_or_404(Post, slug = slug, publish = True)
    comments = Comment.objects.filter(id__in = this_post.comments)
    # print(this_post.get_total_point())

    content = {
        "ThisPost": this_post,
        "Comments": comments,
    }
    return render(request, 'blog/blog-post.html', content)