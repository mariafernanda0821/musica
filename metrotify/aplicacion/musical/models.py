from django.db import models

from datetime import datetime
from aplicacion.usuario.models import *
from djongo import models
from mongoengine import fields
from conection_db import db


album_db=db['album']
playlist_db=db['playlist']

class Track(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    name = models.CharField(max_length=100)
    duration = models.CharField(max_length=10)
    link = models.URLField()

class Album(models.Model):
    id = models.CharField(primary_key=True,max_length=200)
    name = models.CharField(max_length=100)
    description = models.TextField()
    cover = models.URLField()
    published = models.DateTimeField()
    genre = models.CharField(max_length=100)
    artist =models.CharField( max_length=200)
    tracklist = models.ArrayReferenceField(to=Track)

class Playlist(models.Model):
    id = models.CharField(primary_key=True,max_length=200)
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.CharField(max_length=200)
    tracks = models.ArrayReferenceField(to=Track)