from rest_framework import serializers

from imdb.models import Movies, Genre
from django.utils.timezone import now


class MoviesSerializer(serializers.ModelSerializer):
    genre = serializers.SerializerMethodField('get_genre')

    def get_genre(self, obj):
        return [genre.name for genre in obj.genres.all()]

    class Meta:
        model = Movies
        fields = ('genre', 'popularity', 'director', 'imdb_score', 'name')