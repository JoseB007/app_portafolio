from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User

from .models import Proyecto

# Create your views here.
class PortafolioView(generic.TemplateView):
    template_name = 'portafolio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        proyectos = Proyecto.objects.all()
        context['proyectos'] = proyectos

        usuario = User.objects.first()
        context['user'] = usuario
        return context
    

class DetalleProyectoView(generic.DetailView):
    model = Proyecto
    template_name = "detalle_proyecto.html"
    context_object_name = 'proyecto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        usuario = User.objects.first()
        context['user'] = usuario
        return context