from django.urls import path

from . import views

app_name = "usuario_app"

urlpatterns = [
    path(
        'api/registrar', 
        views.UserRegistrationAPIView.as_view(),
        name='api-perfil-registrar',
    ),
     path(
        'registrar', 
        views.RegistroCreateView.as_view(),
        name='auth_registrar',
    ),
    path(
        '', 
        views.LoginView.as_view(),
        name='auth-login',
    ),
    path(
        'perfil-update/<str:pk>/',
        views.UserUpdateView.as_view(),
        name='usuario_update',
    ),
    path('eliminar-cuenta/<str:pk>/', 
         views.UserDeleteView.as_view(), 
         name='eliminar_cuenta'),

    path('cambiar-contrasena/<str:pk>/', 
         views.UpdatePasswordView.as_view(), 
         name='cambiar_password'),

    path(
        'home/', 
        views.HomePruebaView.as_view(),
        name='home',
    ),
    path(
        'detallar-usuario/<str:pk>/usuario/<str:usuario_id>',
        views.UsuarioDetailView.as_view(),
        name='usuario_detallar',
    ),
     path('importar-usuarios/', views.import_users, name='importar_usuarios'),
    path('search-users/', views.search_users, name='search_users'),
     path(
        'prueba/', 
        views.HomePruebaView.as_view(),
        name='home-prueba',
    ),
     path(
        'usuario/logout/', 
        views.LogoutView.as_view(),
        name='usuario-logout',
    ),

]
