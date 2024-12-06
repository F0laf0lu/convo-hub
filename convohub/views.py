from django.views import View
from django.views.generic.base import TemplateView
from django.http import HttpResponse


class HomePageView(TemplateView):
    template_name = 'cover.html'