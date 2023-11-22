
from django.shortcuts import redirect,render
from django.urls import reverse

from .models import Proveedor, Usuario, Servicio, ReservaHora
from .serializers import UsuarioSerializer

from .forms import LoginForm, ReservaForm, ServicioForm, ProveedorForm, ClienteForm

#CREACION API
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status


from datetime import datetime

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
        user = request.POST.get('user',None)
        passw = request.POST.get('password',None)
        try:
            usuario = Usuario.objects.get(user=user)
            if user == usuario.user:
                if passw == usuario.password:
                    if usuario.tipo == 'Empleado':
                        print("Ingreso Exitoso")
                        print(usuario.nombre)
                        user_dic = usuario.to_dict()
                        request.session['usuario']= user_dic
                        request.session['nombre']=usuario.nombre
                        return redirect('empleado')
                    elif usuario.tipo == 'Cliente':
                        print("Ingreso Exitoso")
                        user_dic = usuario.to_dict()
                        request.session['usuario']= user_dic
                        request.session['nombre']=usuario.nombre
                        return redirect('home')
                    elif usuario.tipo == 'Administrador':
                        print("Ingreso Exitoso")
                        return redirect(reverse('admin:index'))
                    else :
                        usuario.delete()
                        print("Usuario tuvo que ser borrado")
                else:
                    print("Pass Invalida")
            else:
                print("User Invalido")
        except Usuario.DoesNotExist:
            print("Usuario no Existe")
            return render(request,'core/login.html', {'form':form})
        
    return render(request,'core/login.html', {'form':form})

def home(request):

    usuario = request.session.get('usuario',{})
    nombre = request.session.get('nombre',{})
    servicios = Servicio.objects.all()
    fecha = datetime.now()
    fecha_actual = fecha.date()


    if request.method == 'POST':
        if 'ReservaFormulario' in request.POST:
            
            fecha = request.POST.get('fecha',None)
            fecha_date = datetime.strptime(fecha, '%Y-%m-%d').date()
            if fecha_date>=fecha_actual:
                try :
                    
                    servicio_nom = request.POST.get('servicio',None)
                    servicio = Servicio.objects.get(nombre=servicio_nom)
                    cliente = Usuario.objects.get(nombre=nombre)
                    
                    
                    reserva=ReservaHora()
                    reserva.fecha_reserva=fecha
                    reserva.servicio=servicio
                    reserva.cliente=cliente
                    reserva.save()
                    print("Reserva Ingresada")
                except Servicio.DoesNotExist:
                    print("Servicio Invalido")
                    return render(request, 'core/home.html', {'usuario':usuario, 'servicios':servicios, 'nombre':nombre})
                

            else:
                print("Fecha Invalida")


    return render(request, 'core/home.html', {'usuario':usuario, 'servicios':servicios, 'nombre':nombre})

def empleado(request):
    usuario = request.session.get('usuario',{})
    nombre = request.session.get('nombre',{})
    reservas = ReservaHora.objects.all()

    if request.method == 'POST':
        
        if 'reserva_realida' in request.POST:
            print("ta bien")
            id_reserva = request.POST.get('reserva', None)
            try :
                reserva = ReservaHora.objects.get(id_reserva=id_reserva)
                reserva.delete()
                return render(request, 'core/empleado.html', {'usuario':usuario, 'nombre':nombre, 'reservas':reservas})
            except ReservaHora.DoesNotExist:
                return render(request, 'core/empleado.html', {'usuario':usuario, 'nombre':nombre, 'reservas':reservas})

        if 'ServicioFormulario' in request.POST:
            form = ServicioForm(request.POST)
            print("Servicio")
            if form.is_valid():
                print("FORMULARIO VALIDO")
                try:
                    servicio = Servicio.objects.get(nombre=form.cleaned_data['nombre'])
                    return redirect('empleado')
                except Servicio.DoesNotExist:
                    servicio = Servicio()
                    servicio.nombre = form.cleaned_data['nombre']
                    servicio.save()
            else:
                print("INVALIDO")
        elif 'ProveedorFormulario' in request.POST:
            form = ProveedorForm(request.POST)
            print(request.POST['nombre'])
            if form.is_valid():
                print("Proveedor Valido")
                proveedor=Proveedor()
                proveedor.nombre = form.cleaned_data['nombre']
                proveedor.fono = form.cleaned_data['fono']
                proveedor.tipo = form.cleaned_data['tipo']
                proveedor.save()
            else :
                print("Datos Mal Ingresados")
        elif 'ClienteFormulario' in request.POST:
            form = ClienteForm(request.POST)
            if form.is_valid():
                cliente=Usuario()
                cliente.user = form.cleaned_data['user']
                cliente.password = form.cleaned_data['password']
                cliente.nombre = form.cleaned_data['nombre']
                cliente.tipo="Cliente"
                cliente.save()
        else:
            print("ta mal")
    return render(request, 'core/empleado.html', {'usuario':usuario, 'nombre':nombre, 'reservas':reservas})