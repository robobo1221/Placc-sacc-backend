from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "backend/index.html"