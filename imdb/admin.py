# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from imdb.models import User, Movies, Genre


@admin.register(Movies)
class MoviesAdmin(admin.ModelAdmin):
    list_display = (
        "popularity", "director", "imdb_score", "name")
    search_fields = ("director", "imdb_score", 'name', "user")
    list_filter = ('director',)
    raw_id_fields = ('user', 'genre')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'reference_no')
    search_fields = ('username', 'reference_no')
    list_filter = ('role',)
    readonly_fields = ('reference_no', )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')
