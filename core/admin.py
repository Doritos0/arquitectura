from django.contrib import admin
from .models import Usuario, Proveedor, Servicio, ReservaHora
# Register your models here.

admin.site.register(Usuario)
admin.site.register(Proveedor)
admin.site.register(Servicio)
admin.site.register(ReservaHora)