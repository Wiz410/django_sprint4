from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModel(models.Model):
    """
    Абстрактная модель.
    Добовляет к модели дату создания.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )

    class Meta:
        abstract = True


class BasePublishedModel(models.Model):
    """
    Абстрактная модель.
    Добавляет к модели флаг публикации.
    """
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )

    class Meta:
        abstract = True


class BaseAuthorModel(models.Model):
    """
    Абстрактная модель.
    Добовляет к модели автора.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )

    class Meta:
        abstract = True


class BaseTitleModel(models.Model):
    """
    Абстрактная модель.
    Добавляет к модели заголовок.
    """
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
    )

    class Meta:
        abstract = True


class Location(BaseModel, BasePublishedModel):
    """Географическая метка"""
    name = models.CharField(
        max_length=256,
        verbose_name='Название места',
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Category(BaseModel, BasePublishedModel, BaseTitleModel):
    """Тематическая категория"""
    description = models.TextField(
        verbose_name='Описание',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, '
            'дефис и подчёркивание.'
        ),
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Post(BaseModel, BaseAuthorModel, BasePublishedModel, BaseTitleModel):
    """Публикация"""
    text = models.TextField(
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        ),
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )
    image = models.ImageField(
        verbose_name='Фото',
        upload_to='post_images',
        blank=True,
    )

    objects = models.Manager()
    published = models.Manager()

    class Meta:
        ordering = [
            '-pub_date',
            'title',
        ]
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title


class Comment(BaseModel, BaseAuthorModel):
    """Комментарий к публикации."""
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comment",
    )

    class Meta:
        ordering = ['created_at', 'author']

    def __str__(self):
        return self.author
