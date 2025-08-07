from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAuthorOrReadOnly
from .forms import ContactForm, RegisterForm, ProfileForm, DocumentForm
from .models import Post, PostForm, Profile, Notification, Document
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import PostSerializer
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import TemplateView


# Create your views here.
@login_required
def home(request):
    posts = Post.objects.all().order_by('-published_date')
    return render(request, 'home.html', {'posts':posts})

@login_required
def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form':form})


@login_required
def create_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("home")  # adjust name as needed
    return render(request, "create_post.html", {"form": form})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post' : post})


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'post_confirm_delete.html', {'post':post})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration Successful")
            return redirect('home')

    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {'form': form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
        messages.error(request, "Invalid Credentials")
    else:
        form = AuthenticationForm()
    return render(request,'registration/login.html', {'form':form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def my_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if request.method == 'POST':
            form.save()
            return redirect('home')

    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})


def blog_filter_view(request):
    query = request.GET.get('q')
    author = request.GET.get('author')
    date = request.GET.get('date')

    posts = Post.objects.all()

    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    elif author:
        posts = posts.filter(author__icontains=author)

    elif date:
        posts = posts.filter(published_date__date=date)

    return render(request, "post_list.html", {'posts':posts})


class PostListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        posts = Post.objects.all().order_by('-id')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostPageView(TemplateView):
    template_name = 'posts_ajax.html'


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    permission_classes = [AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ['author', 'published_date']
    search_fields = ['title', 'content']
    ordering_fields = ['published_date', 'title']
    ordering = ['-published_date']

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)


def notification_view(request):
    notifications = Notification.objects.order_by('-created_at')[:10]
    return render(request, 'notification.html', {'notifications': notifications})


def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('document-list')

    else:
        form = DocumentForm()
    return render(request, 'upload_file.html', {'form': form})


def document_list(request):
    documents = Document.objects.all()
    return render(request, 'documents.html', {'documents': documents})


# token for api for user gurjot, token:  66047499f93ca0685b0ed91abd3b87517b40ca3d

