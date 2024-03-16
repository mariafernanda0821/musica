from django.shortcuts import render
from django.contrib import messages
from django.utils.html import strip_tags
import requests
import json
from itertools import chain
import urllib.request
# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer
from .models import *
from .forms import *
from django.views.generic import (
    ListView, TemplateView, 
    CreateView, UpdateView, DeleteView, DetailView, View ,)
from django.http import JsonResponse
from django.views.generic.edit import (
    FormView
)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
#
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect
from bson import ObjectId
from aplicacion.musical.models import *
from django.db import models

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
)
from django.http import Http404
from .managers import *

# class UserRegistrationAPIView(APIView):
#     def post(self, request):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistroCreateView(FormView):
    model = User
    form_class = RegistroForm
    template_name = 'auth/registro.html'
    success_url = reverse_lazy('usuario_app:auth-login')  # Reemplaza 'ruta_hacia_exitoso' con la URL a la que deseas redirigir después de registrar exitosamente

    def form_valid(self, form):
        #
        User.objects.create_user(
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            type=form.cleaned_data['type'],
            name=form.cleaned_data['name'],
            username=form.cleaned_data['username']
        )
        # enviar el codigo al email del user
        return super(RegistroCreateView, self).form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '¡Error! Por favor, corrige los errores en el formulario.')
        
        return self.render_to_response(self.get_context_data(form=form))


class LoginView(FormView):
    template_name = 'auth/login.html'
    model=User
    form_class = LoginForm
    success_url = reverse_lazy('usuario_app:home')
    
    def form_valid(self, form):
        try:
            user = User.objects.get(email=form.cleaned_data['email'])
            print("usuario no registrado ", user)
            if user.is_deleted:
                messages.error(self.request, 'Correo  electronico no registrado.' )
                return self.render_to_response(self.get_context_data(form=form))
        except User.DoesNotExist :
                messages.error(self.request, 'Correo  electronico no registrado.')
                return self.render_to_response(self.get_context_data(form=form))

        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        if user is not None:
            login(self.request, user)
            print("if user is not None:")
            return super(LoginView, self).form_valid(form)
        else:
            error_message = 'Credenciales inválidas. Por favor, inténtalo de nuevo.' 
            messages.error(self.request, 'Credenciales inválidas. Por favor, inténtalo de nuevo.' )
       
            return self.render_to_response(self.get_context_data(form=form))
        
    def form_invalid(self, form):
        # Dentro de tu método de vista
        messages.error(self.request, 'Credenciales inválidas. Por favor, inténtalo de nuevo.' )
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(View):
    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'usuario_app:auth-login'
            )
        )


class UserUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "usuario/updatePerfil.html"
    form_class = UserUpdateForm
    model = User
    context_object_name = "usuario"
    success_url =reverse_lazy('usuario_app:home')
    
    def get_object(self, queryset=None):
        user_id = self.kwargs.get('pk')
        user = User.objects.get(id=user_id)
        return user #User.objects.get(id=ObjectId(user_id))


class UserDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print(pk)
        user_id = pk #self.kwargs.get('pk')
        
        user = User.objects.get(id=user_id) #User.objects.get(_id=ObjectId(user_id))
        user.is_deleted = True
        user.email= user.email + "eliminado"
        user.save()
       
        return HttpResponseRedirect(
            reverse(
                'usuario_app:auth-login'
            )
        )


class UpdatePasswordView(LoginRequiredMixin, FormView):
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')
    login_url = reverse_lazy('users_app:user-login')

    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            email=usuario.email,
            password=form.cleaned_data['password1']
        )

        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()

        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)



def import_users(request):
    urlLinkUsuario = 'https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/users.json'
    urlMusica='https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/albums.json'
    urlPl=' https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/playlists.json'
    
    try:
        response = requests.get(urlLinkUsuario)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        responseMusica = requests.get(urlMusica)
        responseMusica.raise_for_status()  # Raise an exception for non-2xx status codes
        
        responsePlay = requests.get(urlPl)
        responsePlay.raise_for_status()  # Raise an exception for non-2xx status codes
        
        if response.status_code == 200 and responseMusica.status_code == 200 and responsePlay.status_code == 200:
            # data = json.loads(response.content)
            # dataMusica=json.loads(responseMusica.content)
            # dataPlay=json.loads(responsePlay.content)
            # usuario_db.insert_many(data)
            # for user_data in data:
            #     print(user_data)
            #     user = User.objects.create_user(
            #         id=user_data['id'],
            #         name=user_data['name'],
            #         email=user_data['email'],
            #         username=user_data['username'],
            #         type=user_data['type'],
            #         password="123456"
            #     )
            #     user.save()
        
            # for musica_data in dataMusica:
            #     artist_id = musica_data['artist']
            #     print("artist_id ", artist_id)
            #     print("artist_id ", musica_data)
            #     album = Album.objects.create(
            #         id=data['id'],
            #         name=musica_data['name'],
            #         description=musica_data['description'],
            #         cover=musica_data['cover'],
            #         published=datetime.strptime(musica_data['published'], '%Y-%m-%dT%H:%M:%S.%fZ'),
            #         genre=musica_data['genre'],
            #         artist=musica_data['artist']
            #     )
            #     for i in range(len(data['tracklist'])): 

            #         track_data = data['tracklist'][i]
            #         track = Track.objects.create(
            #             id=track_data['id'],
            #             name=track_data['name'],
            #             duration=track_data['duration'],
            #             link=track_data['link']
            #         )
            #         track.save()
            #         album.tracklist.append(ObjectId(track._id))

            #     album.save()

            # for play_data in dataPlay:
               
            #     creator_id = play_data['artist']
            #     creator = User.objects.get(id=creator_id)

            #     playList = Playlist.objects.create(
            #         id=play_data['id'],
            #         name=play_data['name'],
            #         description=play_data['description'],
            #         creator=creator,
                    
            #     )
            #     playList_data = play_data['tracklist']
            #     for list in playList_data:
            #         creatorPlayList = Track.objects.get(id=list)
            #         playList.tracks.append(creatorPlayList)

            #     playList.save()


            return  HttpResponseRedirect(reverse('usuario_app:auth-login'))
    
    except Exception as e:
        # Manejar cualquier error que pueda ocurrir durante la importación de usuarios
        # Puedes mostrar un mensaje de error o realizar alguna otra acción aquí
        print(f"Error al importar usuarios: {e}")
        return    HttpResponseRedirect(reverse('usuario_app:auth-login'))
    
    
# def search_users(request):
#     if request.method == 'GET':
#         search_query = request.GET.get('q', '')  # Obtiene el parámetro de búsqueda de la URL
#         users = User.objects.filter(name__icontains=search_query)  # Filtra los usuarios cuyo nombre contiene la consulta de búsqueda
#         return render(request, 'search_users.html', {'users': users, 'search_query': search_query})
    
# def search_users(request):
#     if request.is_ajax():
#         search_query = request.GET.get('search_query', '')
#         users = User.objects.filter(name__icontains=search_query)
#         user_names = [user.name for user in users]
#         print(user_names)
#         return JsonResponse({'user_names': user_names})
#     else:
#         return render(request, 'search_users.html')
    
def search_users(request):
    print("estoy en la search_users")
    query = request.GET.get('query', '')
    print(query)
    print("********************")
    # resultados = usuario_db.find({"name":'Mercedes Ortega Mayorga'})
    # print("estoy en la search_users", resultados)
    # regex = re.compile(nombre_a_buscar, re.IGNORECASE)
    # # Crea la consulta para buscar por el campo "nombre" utilizando la expresión regular
    # query = { "nombre": { "$regex": regex } }
    # # Realiza la búsqueda en la colección "usuarios"
    # resultados = collection.find(query)
    # users = User.objects.filter(name__icontains=query) # Realiza la búsqueda de usuarios por nombre
    return render(request, 'searchUsuario.html', {'users': []})


class UpdatePasswordView(LoginRequiredMixin, FormView):
    form_class = UpdatePasswordForm
    template_name = "usuario/updatePerfil.html"
    success_url = reverse_lazy('usuario:usuario_update')
    #login_url = reverse_lazy('auth-login')

    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            email=usuario.email,
            password=form.cleaned_data['password1']
        )

        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()

        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)
    


class UsuarioDetailView(LoginRequiredMixin, DetailView):
    template_name = "usuario/home_detallar_usuario.html"
    model = User

    def get_object(self, queryset=None):
        # Obtener el ID del usuario desde los parámetros de la URL
        usuarioId = self.kwargs.get('usuario_id')
        pk = self.kwargs.get('pk')

        try:
            usuarioSearch =  User.objects.get(id=usuarioId) #User.objects.get(pk=usuarioId)
            userId =  User.objects.get(id=pk) #User.objects.get(pk=pk)
        except User.DoesNotExist:
            # Si el usuario no existe, lanzar un error 404
            raise Http404("El usuario no existe")
        
        return userId,usuarioSearch

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userId, usuarioSearch = self.object
    
        albunes = Album.objects.filter(artist=usuarioSearch.id)
        playlist = Playlist.objects.filter(creator=usuarioSearch.id)
        
        context['usuario'] = userId
        context['usuarioSearch'] = usuarioSearch
        context['albunesArray'] = albunes
        context['playlistArray'] = playlist
        
        return context


  
class HomePruebaView(LoginRequiredMixin, TemplateView):
    template_name = 'usuario/home.html'; 
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            # Obtener el objeto completo del usuario autenticado
            user = self.request.user
            albunes = Album.objects.filter(artist=user.id)
            playlist =Playlist.objects.filter(creator=user.id)

            print(playlist)
            playlist_duplicada = list(chain.from_iterable([playlist] * 3))
            context['usuario'] = user
            context['albunesArray'] = playlist
            context['playlistArray'] = playlist_duplicada 
            # Si tienes campos personalizados en tu modelo de usuario, puedes acceder a ellos de la misma manera
            return context

class HomeUsuarioView(LoginRequiredMixin, TemplateView):
    template_name = 'usuario/homeUsuario.html'; 
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            # Obtener el objeto completo del usuario autenticado
            user = self.request.user
            albunes = Album.objects.filter(artist=user.id)
            playlist =Playlist.objects.filter(creator=user.id)
            playlist_duplicada = list(chain.from_iterable([playlist] * 3))
            context['usuario'] = user
            context['albunesArray'] = albunes
            context['playlistArray'] = playlist_duplicada 
            # Si tienes campos personalizados en tu modelo de usuario, puedes acceder a ellos de la misma manera
            return context


class UserRegistrationAPIView(CreateAPIView):
    
    serializer_class = UserRegistrationSerializer



# class LoginView(View):
#     template_name = 'usuario/login.html'

#     def get(self, request):
#         return render(request, self.template_name)

#     def post(self, request):
#         correo = request.POST.get('correo')
#         password = request.POST.get('password')

#         if not correo or not password:
#             errors = {'error': 'Se requieren el correo de usuario y la contraseña'}
#             return render(request, self.template_name, {'errors': errors})

#         user = authenticate(request, correo=correo, password=password)

#         if user is None:
#             errors = {'error': 'Credenciales inválidas. Por favor, inténtalo de nuevo.'}
#             return render(request, self.template_name, {'errors': errors})

#         # Si la autenticación es exitosa, puedes redirigir a una página de éxito o hacer lo que necesites aquí
#         return render(request, 'usuario/exito.html')  # Reemplaza 'usuario/exito.html' con la ruta a tu template de éxito
