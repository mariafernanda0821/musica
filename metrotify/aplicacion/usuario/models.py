from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import Group
from .managers import *
from djongo import models
from aplicacion.musical.models import * 
from aplicacion.musical.forms import * 
from conection_db import db

usuario_db=db['usuario']

class User(AbstractBaseUser,TimeStampedModel,PermissionsMixin):
    NOMBRE_CHOICES = [
        ('Musico', 'listener'),
        ('Escuchas', 'musician'),
    ]
    id = models.CharField(primary_key=True, max_length=200)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    type = models.CharField(max_length=30, choices=NOMBRE_CHOICES)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='usuario_groups')
    is_deleted=models.BooleanField(default=False)
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_user_permissions',
        blank=True,
        help_text='The permissions this user has.',
        verbose_name='user permissions',
    )
    
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name']

    objects = UserManager()
    
    def __str__(self):
        return self.name

