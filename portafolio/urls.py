from django.urls import path

from . import views

urlpatterns = [
    path("", views.PortafolioView.as_view(), name="portafolio"),
    path("proyecto/<str:slug>/", views.DetalleProyectoView.as_view(), name="detalle-proyecto"),
]