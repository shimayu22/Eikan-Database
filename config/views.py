from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import TemplateView

# Create your views here.
class IndexView(TemplateView):
    template_name = 'config/index.html'