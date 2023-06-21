from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect

from .models import Post, Comment


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


class CommentDispacthMixin:
    """
    Вспомогательный класс.
    Переопределяет dispatch, для получения и проверки автора комментария.
    """
    def dispatch(self, request, *args, **kwargs):
        posts = get_object_or_404(Comment, id=self.kwargs['comment_id'])
        if request.user != posts.author:
            return redirect('blog:post_detail', post_id=posts.pk)
        return super().dispatch(request, *args, **kwargs)
