from django import forms

class LoginForm(forms.Form):
    user = forms.CharField(max_length=20, min_length=4, required=True)
    password = forms.CharField(max_length=20, min_length=4, required=True)

class ReservaForm(forms.Form):
    fecha = forms.DateField( required=True)
    servicio = forms.CharField(required=True)

class ServicioForm(forms.Form):
    nombre = forms.CharField(max_length=30, required=True)

class ProveedorForm(forms.Form):
    nombre = forms.CharField(max_length=25, required=True)
    fono = forms.IntegerField(required=True)
    tipo = forms.CharField(max_length=30, required=True)

class ClienteForm(forms.Form):
    user = forms.CharField(max_length=20, required=True)
    password = forms.CharField(max_length=20, required=True)
    nombre = forms.CharField(max_length=80, required=True)