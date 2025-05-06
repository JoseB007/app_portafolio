from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
from django.db import models

class Proyecto(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(
        blank=True, null=True, 
        unique=True, help_text="URL amigable, se genera automáticamente"
    )
    descripcion = models.TextField()
    resumen = models.TextField(blank=True, help_text="Un resumen breve que se muestra en tarjetas")
    tecnologias = models.TextField(help_text="Ej: Django, PostgreSQL, Bootstrap")
    caracteristicas = models.TextField(blank=True, help_text="Características incluidas en el proyecto")
    arquitectura = models.TextField(blank=True, help_text="Arquitectura usada para la construcción")
    
    imagen_miniatura = models.FileField(
        upload_to='proyectos/miniaturas/', 
        blank=True, null=True, 
        help_text="Solo se permiten archivos .SVG"
    )
    
    github_url = models.URLField(blank=True, null=True)
    demo_url = models.URLField(blank=True, null=True)

    retos = models.TextField(blank=True)
    proximos_pasos = models.TextField(blank=True)

    visible = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('detalle-proyecto', args=[self.slug])
    
    def tecnologias_formateadas(self):
        lineas = self.tecnologias.splitlines()
        resultado = []
        for linea in lineas:
            if ':' in linea:
                parte1, parte2 = linea.split(':', 1)
                html = f"<li><strong>{parte1.strip()}:</strong> {parte2.strip()}</li>"
            else:
                html = f"<li>{linea.strip()}</li>"
            resultado.append(html)
        return '\n'.join(resultado)
    
    def get_imagen(self):
        if self.imagen_miniatura:
            return self.imagen_miniatura.url
        return '/static/img/miniatura.svg'
    
    def save(self, *args, **kwargs):
        # Genera el slug automáticamente si no se proporciona uno
        if not self.slug:
            self.slug = slugify(self.titulo)
    
        super().save(*args, **kwargs)


