from django.urls import path
from .views import login, lista_usuarios, detalle_usuario

urlpatterns=[
    path('', login, name="login"),
    path('lista_usuarios', lista_usuarios, name="lista_usuarios"),
    path('detalle_usuario/<id>', detalle_usuario, name="detalle_usuario"),
]