
from django.shortcuts import redirect,render

from .models import Usuario
from .serializers import UsuarioSerializer

from .forms import LoginForm

#CREACION API
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

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
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = UsuarioSerializer(usuario,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    if request.method =='DELETE':
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


def login (request):
    
    form = LoginForm()

    if request.method == 'POST':
        query = Usuario.objects.all()
        serializer = UsuarioSerializer(query, many = True)
        print(serializer.data)
        users= Usuario.objects.values_list('user', flat=True)
        contras = Usuario.objects.values_list('password', flat=True)
        print(users)
        lista_users = list(users)
        lista_pass = list(contras)
        user = request.POST.get('user',None)
        passw = request.POST.get('password',None)
        if user in lista_users:
            i=lista_users.index(user)
            if lista_pass[i] == passw:
                return render(request, 'core/home.html')
            #if de tipo de usuario redirige a distintos templates
        else:
            print("Invalido")


    return render(request,'core/login.html', {'form':form})

'''
 if request.method == 'POST':
        query = Usuario.objects.all()
        serializer = UsuarioSerializer(query, many = True)
        Usuarios=Usuario.objects.all('user', flat=True)
        Contraseñas=Usuario.objects.values_list('password', flat=True)
        user = request.POST.get('user',None)
        password = request.POST.get('password', None)
        print(serializer.data)
        if user in Usuarios:
            if password in Contraseñas:
                print("Valido")
'''