
from django import forms
from .models import *

from django.contrib.auth import authenticate

class RegistroForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
                'class':  'form-control',
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir Contraseña',
                'class':  'form-control',
            }
        )
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'username', 'type']
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': 'Correo Electronico ...','class': 'form-control'}, ),
            'username': forms.TextInput(
                attrs={'placeholder': 'Usuario ...','class': 'form-control'}, ),
            'email': forms.EmailInput(attrs={'placeholder': 'Nombre y Apellido ...', 'class': 'form-control'},),
            'type': forms.Select(attrs={'placeholder': 'Tipo de Usuario ...','class': 'form-control'}),
        }

        def clean_password2(self):
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                self.add_error('password2', 'Las contraseñas no son iguales')


class LoginForm(forms.Form):
    email = forms.CharField(
        label='Correo Electronico',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Correo Electronico',
            }
        )
    )
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'contraseña'
            }
        )
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        print("entre aqui incorrecta las user", email, "password",  password)
        if not email:
            raise forms.ValidationError('El correo electrónico es obligatorio.')
        if not password:
            raise forms.ValidationError('La contraseña es obligatoria.')
            
        return self.cleaned_data
    


class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model = User  # Especifica la clase de modelo User
        fields = ['name', 'email', 'username', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nombre y Apellido ...','class': 'form-control'}),
            'username': forms.TextInput(attrs={'placeholder': 'Usuario ...','class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo Electronico ...', 'class': 'form-control'}),
            'type': forms.Select(attrs={'placeholder': 'Tipo de Usuario ...','class': 'form-control'}),
        }



class UpdatePasswordForm(forms.Form):

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Actual'
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Nueva'
            }
        )
    )