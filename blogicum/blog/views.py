# from django.http import HttpResponse, HttpRequest
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
    PaginatorMixin,
    ProfileMixin,
    PostMixin,
    CommentMixin,
    CommentDispacthMixin,
    PostDispatchMixin,
    PostFormMixin,
    URLPostMixin,
    URLProfileMixin,
)
from .forms import CommentForm, UserForm
from .models import Post, Category, Comment

DATENOW = timezone.now()

User = get_user_model()


class IndexListView(
    PostMixin,
    PaginatorMixin,
    ListView
):
    """Главная страница."""
    template_name = 'blog/index.html'

    def get_queryset(self):
        return Post.objects.filter(
            Q(pub_date__lte=DATENOW)
            & Q(is_published=True)
            & Q(category__is_published=True)
        ).order_by('-pub_date').annotate(comment_count=Count('comment'))


class PostDetailView(
    PostMixin,
    DetailView
):
    """Страница поста."""
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
    PostMixin,
    PostFormMixin,
    LoginRequiredMixin,
    URLProfileMixin,
    CreateView
):
    """Создание поста."""

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditPostUpdateView(
    PostMixin,
    PostFormMixin,
    PostDispatchMixin,
    LoginRequiredMixin,
    URLPostMixin,
    UpdateView
):
    """Редактирование поста."""
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.kwargs['post_id']
        return super().form_valid(form)


class DeletePostDeleteView(
    PostMixin,
    PostFormMixin,
    PostDispatchMixin,
    LoginRequiredMixin,
    URLProfileMixin,
    DeleteView
):
    """Удаление поста."""
    pk_url_kwarg = 'post_id'


class CategoryPostsListView(
    PostMixin,
    PaginatorMixin,
    ListView
):
    """Страница с категориями."""
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


class ProfileListView(
    ProfileMixin,
    PaginatorMixin,
    ListView
):
    """Страница профиля."""
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
    ProfileMixin,
    LoginRequiredMixin,
    URLProfileMixin,
    UpdateView
):
    """Редактивование страници профиля."""
    form_class = UserForm
    template_name = 'blog/user.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_object(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        return super().get_object()


class CommentCreateView(
    CommentMixin,
    LoginRequiredMixin,
    URLPostMixin,
    CreateView
):
    """Создание комментария."""
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
    CommentMixin,
    CommentDispacthMixin,
    LoginRequiredMixin,
    URLPostMixin,
    UpdateView
):
    """Редактирование комментария."""


class DeleteCommentDeleteView(
    CommentMixin,
    CommentDispacthMixin,
    LoginRequiredMixin,
    URLPostMixin,
    DeleteView
):
    """Удаление комментария."""
