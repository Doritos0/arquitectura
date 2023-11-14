from django.shortcuts import redirect,render

from .models import Usuario
from .serializers import UsuarioSerializer

#CREACION API
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser

# Create your views here.

@csrf_exempt
@api_view(['GET','POST'])
def lista_usuarios (request):
    if request.method == 'GET':
        query = Usuario.objects.all()
        serializer = UsuarioSerializer(query, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            user = request.POST.get('user', None)
            if user in Usuario.objects.values_list('user', flat=True):
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else: 
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def detalle_usuario (request,id):
    try:
        usuario = Usuario.objects.get(user=id)
    except Producto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serilizer = UsuarioSerializer(usuario)
        return Response(serilizer.data)
    if request.method == 'PUT':
        serializer = UsuarioSerializer(usuario,data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data)
        else:
            return Response(serilizer.errors,status=status.HTTP_404_NOT_FOUND)
    if request.method =='DELETE':
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 

def login (request):
    return render(request,'core/login.html')