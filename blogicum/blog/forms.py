from django import forms
from django.contrib.auth import get_user_model

from .models import Post, Comment  # , Profile

User = get_user_model()


class PostForm(forms.ModelForm):
    """
    Форма для модели публикаций.
    """

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }


class CommentForm(forms.ModelForm):
    """
    Форма для модели комментариев.
    """

    class Meta:
        model = Comment
        fields = ('text',)


class UserForm(forms.ModelForm):
    """
    Форма для редактирования профиля.
    """

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )
