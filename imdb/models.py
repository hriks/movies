# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.utils.crypto import get_random_string

import uuid


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=32, choices=(
        ('admin', 'Admin'),
        ('user', 'user')
    ), default='user', db_index=True)
    reference_no = models.CharField(max_length=15, null=True, blank=True)
    username = models.CharField(max_length=24)

    def save(self, *args, **kwargs):
        if self.reference_no is None:
            self.assignReferenceNumber()
        super(User, self).save(*args, **kwargs)

    def assignReferenceNumber(self):
        temp_ref = 'imdb:' + get_random_string(10, allowed_chars='3456789')
        while User.objects.filter(reference_no=temp_ref).exists():
            temp_ref = 'imdb:' + get_random_string(10, allowed_chars='3456789')
        self.reference_no = temp_ref


class Movies(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ManyToManyField('User')
    popularity = models.FloatField()
    director = models.CharField(max_length=128)
    genre = models.ManyToManyField('Genre')
    imdb_score = models.FloatField()
    name = models.CharField(max_length=128)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        try:
            current = Movies.objects.get(id=self.id)
            if current.genre != self.genre:
                self.genre += (', ' + self.genre)
        except Movies.DoesNotExist:
            pass
        super(Movies, self).save(*args, **kwargs)


class Genre(models.Model):
    name = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
