from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils import timezone
from .models import Post

# 👤 Register View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # or 'post_list'
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# 🏠 Dashboard View
@login_required
def dashboard(request):
    return render(request, 'blog/dashboard.html')

# 📝 Create Post View
@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            Post.objects.create(
                title=title,
                content=content,
                author=request.user,
                created_at=timezone.now()
            )
            return redirect('post_list')
    return render(request, 'blog/create_post.html')

# 📄 Blog List View
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

# 📃 Blog Detail View
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
