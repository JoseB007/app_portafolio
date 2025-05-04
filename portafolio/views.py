from django.shortcuts import render
from django.views import generic

from .models import Proyecto

# Create your views here.
class PortafolioView(generic.TemplateView):
    template_name = 'portafolio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        proyectos = Proyecto.objects.all()
        context['proyectos'] = proyectos
        return context
    

class DetalleProyectoView(generic.DetailView):
    model = Proyecto
    template_name = "detalle_proyecto.html"
    context_object_name = 'proyecto'