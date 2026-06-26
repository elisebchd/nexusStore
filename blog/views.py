from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post, BlogCategory


def academy_home(request):
    posts = Post.objects.filter(status='published').order_by('-published_at')
    categories = BlogCategory.objects.all()
    featured = posts.first()
    recent = posts[1:7]
    paginator = Paginator(posts, 9)
    page = request.GET.get('page')
    posts_page = paginator.get_page(page)
    return render(request, 'blog/academy.html', {
        'posts': posts_page,
        'featured': featured,
        'recent': recent,
        'categories': categories,
    })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    post.views += 1
    post.save(update_fields=['views'])
    related = Post.objects.filter(status='published', category=post.category).exclude(id=post.id)[:3]
    return render(request, 'blog/post_detail.html', {'post': post, 'related': related})
