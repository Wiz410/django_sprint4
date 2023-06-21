from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.utils import timezone
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import get_object_or_404

from .mixins import (
    CommentDispacthMixin,
    PostDispatchMixin,
    URLPostMixin,
    URLProfileMixin,
)
from .forms import CommentForm, UserForm, PostForm
from .models import Post, Category, Comment

POST_PER_PAGE: int = 10

DATENOW = timezone.now()

User = get_user_model()


class IndexListView(ListView):
    """Главная страница."""
    model = Post
    paginate_by = POST_PER_PAGE
    template_name = 'blog/index.html'

    def get_queryset(self):
        return Post.objects.filter(
            Q(pub_date__lte=DATENOW)
            & Q(is_published=True)
            & Q(category__is_published=True)
        ).order_by('-pub_date').annotate(comment_count=Count('comment'))


class PostDetailView(DetailView):
    """Страница поста."""
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (Comment.objects.select_related(
            'author'
        ).filter(
            post_id=self.kwargs['post_id']
        ))
        return context


class CreatePostCreateView(
    URLProfileMixin,
    LoginRequiredMixin,
    CreateView
):
    """Создание поста."""
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditPostUpdateView(
    PostDispatchMixin,
    URLPostMixin,
    LoginRequiredMixin,
    UpdateView
):
    """Редактирование поста."""
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.kwargs['post_id']
        return super().form_valid(form)


class DeletePostDeleteView(
    PostDispatchMixin,
    URLProfileMixin,
    LoginRequiredMixin,
    DeleteView
):
    """Удаление поста."""
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'


class CategoryPostsListView(ListView):
    """Страница с категориями."""
    model = Post
    paginate_by = POST_PER_PAGE
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

    def get_queryset(self):
        self.category = get_object_or_404(
            Category.objects.filter(
                Q(slug=self.kwargs['category_slug'])
                & Q(is_published=True)
            ),
            slug=self.kwargs['category_slug']
        )
        return Post.objects.all().filter(
            Q(pub_date__lte=DATENOW)
            & Q(category__slug=self.kwargs['category_slug'])
            & Q(is_published=True)
        ).order_by('-pub_date').annotate(comment_count=Count('comment'))


class ProfileListView(ListView):
    """Страница профиля."""
    model = User
    paginate_by = POST_PER_PAGE
    template_name = 'blog/profile.html'
    slug_url_kwarg = 'username'

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        return Post.objects.all().filter(
            author=self.author
        ).order_by('-pub_date').annotate(
            comment_count=Count('comment')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.author
        return context


class ProfilUpdateView(
    URLProfileMixin,
    LoginRequiredMixin,
    UpdateView
):
    """Редактивование страници профиля."""
    model = User
    form_class = UserForm
    template_name = 'blog/user.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_object(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        return super().get_object()


class CommentCreateView(
    URLPostMixin,
    LoginRequiredMixin,
    CreateView
):
    """Создание комментария."""
    model = Comment
    posts = None
    form_class = CommentForm
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        self.posts = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.posts
        return super().form_valid(form)


class EditCommentUpdateView(
    CommentDispacthMixin,
    URLPostMixin,
    LoginRequiredMixin,
    UpdateView
):
    """Редактирование комментария."""
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'


class DeleteCommentDeleteView(
    CommentDispacthMixin,
    URLPostMixin,
    LoginRequiredMixin,
    DeleteView
):
    """Удаление комментария."""
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'
