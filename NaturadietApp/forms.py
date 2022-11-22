from django import forms
import django
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from .models import Usuario
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = "__all__"


class DietaForm(UserCreationForm):
    
    class Meta:
        model = Usuario
        fields = [ 
            'edad',
            'altura',
            'peso',
        ]
        labels = {
            'edad': '', 
            'altura': '', 
            'peso': '',
        }
        
        


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
    label="",
    strip=False,
    widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña*'}),
    help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
    label="",
    strip=False,
    widget=forms.PasswordInput(attrs={'placeholder': 'Repetir Contraseña*'}),
    )


    class Meta:
        model = Usuario
        fields = [
            'username', 
            'email', 
            'password1', 
            'password2', 
            'first_name', 
            'last_name', 
            'edad',
            'dni',
            'telefono',
            'localidad',
            'provincia',
            'direccion',
            'cp',
            'altura',
            'peso',
            'genero',
        ]
        labels = {
            'username': '', 
            'email': '',
            'first_name': '', 
            'last_name': '', 
            'edad': '',
            'dni': '',
            'telefono': '',
            'provincia': '',
            'localidad': '',
            'direccion': '',
            'cp': '',
            'altura': '',
            'peso': '',
            'genero': '',
        }
        widgets = {
            'username': forms.TextInput(
                attrs = {
                    'placeholder': 'Usuario*'
                }
            ),
            'email': forms.EmailInput (
                attrs = {
                    'placeholder': 'Email*'
                }
            ),
            'first_name': forms.TextInput (
                attrs = {
                    'placeholder': 'Nombre*'
                }
            ),
            'last_name': forms.TextInput (
                attrs = {
                    'placeholder': 'Apellidos*'
                }
            ),
            'edad': forms.TextInput (
                attrs = {
                    'placeholder': 'Edad*'
                }
            ),
            'dni': forms.TextInput (
                attrs = {
                    'placeholder': 'Dni*'
                }
            ),
            'telefono': forms.TextInput (
                attrs = {
                    'placeholder': 'Teléfono*'
                }
            ),
            'provincia': forms.Select (
                attrs = {
                    'initial': 'Provincia*'
                }
            ),
            'localidad': forms.TextInput (
                attrs = {
                    'placeholder': 'Localidad*'
                }
            ),
            'direccion': forms.TextInput (
                attrs = {
                    'placeholder': 'Dirección*'
                }
            ),
            'cp': forms.TextInput (
                attrs = {
                    'placeholder': 'C.P*'
                }
            ),
            'altura': forms.NumberInput (
                attrs = {
                    'placeholder': 'Altura*'
                }
            ),
            'peso': forms.TextInput (
                attrs = {
                    'placeholder': 'Peso*'
                }
            ),
            'genero': forms.Select (
                attrs = {
                    'placeholder': 'Género*'
                }
            ),
            
            
        }
        #help_texts = { k:"" for k in fields }


