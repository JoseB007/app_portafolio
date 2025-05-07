from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
from django.db import models

class Portafolio(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portafolio')
    titulo_principal = models.CharField(max_length=200)
    descripcion_general = models.TextField(blank=True, null=True)
    mensaje_bienvenida = models.CharField(max_length=200)
    resumen_profesional = models.TextField()
    mision = models.TextField(blank=True, null=True)
    imagen = models.FileField(
        upload_to='portafolio/',
        blank=True, null=True,
    )

    class Meta:
        verbose_name = "Portafolio"
        verbose_name_plural = "Portafolios"

    def __str__(self):
        return f"Portafolio de {self.usuario.persona}"

    def get_imagen(self):
        if self.imagen:
            return self.imagen.url
        return '/static/img/profile.svg'   


class Persona(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='persona')
    nombre_completo = models.CharField(max_length=200, help_text="Nombre completo de la persona")
    ocupacion = models.CharField(max_length=200, blank=True, null=True)
    correo_electronico = models.EmailField(blank=True, null=True)
    numero_telefono = models.CharField(max_length=20, blank=True, null=True)
    hoja_de_vida = models.FileField(upload_to='documentos/', blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"

    def __str__(self):
        return self.nombre_completo 
    
    def get_redes_sociales(self):
        return {
            'GitHub': self.github,
            'LinkedIn': self.linkedin,
        }


class Stack(models.Model):
    persona = models.ForeignKey('Persona', on_delete=models.CASCADE, related_name='stacks')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    icono = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Stack"
        verbose_name_plural = "Stacks"

    def __str__(self):
        return f"{self.nombre} ({self.persona.nombre_completo})"

class Proyecto(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(
        blank=True, null=True, 
        unique=True, help_text="URL amigable, se genera automáticamente (máx. 50 palabras)"
    )
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
    creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['-creacion']

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


