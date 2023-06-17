from django.views.generic import TemplateView
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


class AboutTemplateView(TemplateView):
    """Страница о проекте."""
    template_name = 'pages/about.html'


class RulesTemplateView(TemplateView):
    """Страница с правилами проекта."""
    template_name = 'pages/rules.html'


def csrf_failure(request: HttpRequest, reason='') -> HttpResponse:
    """Ошибка проверки CSRF: 403."""
    template = 'pages/403csrf.html'
    return render(
        request,
        template,
        status=403,
    )


def page_not_found(request: HttpRequest, exception) -> HttpResponse:
    """Ошибка страница не найдена: 404."""
    template = 'pages/404.html'
    return render(
        request,
        template,
        status=404,
    )


def server_error(request: HttpRequest) -> HttpResponse:
    """Ошибка сервера: 500."""
    template = 'pages/500.html'
    return render(
        request,
        template,
        status=500,
    )
