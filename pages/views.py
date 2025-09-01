from django.views.generic import TemplateView
from django.shortcuts import render


# Create your views here.
class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"
