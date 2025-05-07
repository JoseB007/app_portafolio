from django.contrib import admin

from .models import Portafolio, Persona, Proyecto, Stack

# Register your models here.
@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ("nombre_completo", "ocupacion", "correo_electronico", "numero_telefono")


admin.site.register(Portafolio)
admin.site.register(Proyecto)
admin.site.register(Stack)
