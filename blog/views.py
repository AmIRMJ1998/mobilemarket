from django.shortcuts import render

# Create your views here.
def blogIndex(request):
    return render(request, 'blog/blog-index.html')

def blogPost(request):
    return render(request, 'blog/blog-post.html')