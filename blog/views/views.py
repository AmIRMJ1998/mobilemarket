from django.shortcuts import get_object_or_404
from django.shortcuts import render
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

    content = {
        "ThisPost": this_post,
    }
    return render(request, 'blog/blog-post.html', content)