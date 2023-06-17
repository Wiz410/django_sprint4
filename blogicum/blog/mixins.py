from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect

from .models import Post, Comment
from .forms import PostForm, CommentForm

POST_PER_PAGE: int = 10

DATENOW = timezone.now()

User = get_user_model()


class PaginatorMixin:
    """
    Вспомогательный класс.
    Добовляет разделение списка постов на страницы.
    """
    paginate_by = POST_PER_PAGE


class ProfileMixin:
    """
    Вспомогательный класс.
    Указывает модель User для класса.
    """
    model = User


class PostMixin:
    """
    Вспомогательный класс.
    Указывает модель Post для класса.
    """
    model = Post


class CommentMixin:
    """
    Вспомогательный класс.
    Указывает модель Comment для класса.
    """
    model = Comment


class CommentDispacthMixin:
    """
    Вспомогательный класс.
    Указывает форму CommentForm.
    Шаблон comment.html.
    И переопределяет dispatch, для получения и проверки автора комментария.
    """
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        posts = get_object_or_404(Comment, id=self.kwargs['comment_id'])
        if request.user != posts.author:
            return redirect('blog:post_detail', post_id=posts.pk)
        return super().dispatch(request, *args, **kwargs)


class PostDispatchMixin:
    """
    Вспомогательный класс.
    Переопределяет dispatch, для получения и проверки автора публикации.
    """
    def dispatch(self, request, *args, **kwargs):
        posts = get_object_or_404(Post, id=self.kwargs['post_id'])
        if request.user != posts.author:
            return redirect('blog:post_detail', post_id=posts.pk)
        return super().dispatch(request, *args, **kwargs)


class PostFormMixin:
    """
    Вспомогательный класс.
    Указывает форму PostForm.
    И шаблон create.html
    """
    form_class = PostForm
    template_name = 'blog/create.html'


class URLPostMixin:
    """
    Вспомогательный класс.
    Переопределяет get_success_url, для переадресовки на страницу поста.
    """
    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class URLProfileMixin:
    """
    Вспомогательный класс.
    Переопределяет get_success_url, для переадресовки на страницу профиля.
    """
    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user}
        )
