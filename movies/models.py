from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    duration = models.IntegerField(null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    poster_url = models.TextField(null=True, blank=True)
    genres = models.CharField(max_length=255, null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)
    mood = models.CharField(max_length=100, null=True, blank=True)
    age_rating = models.CharField(max_length=10, null=True, blank=True)
    director = models.CharField(max_length=255, null=True, blank=True)
    average_rating = models.FloatField(null=True, blank=True)
    awards = models.TextField(null=True, blank=True)
    available_on = models.CharField(max_length=255, null=True, blank=True)
    available_languages = models.CharField(max_length=255, null=True, blank=True)
    actor_1 = models.CharField(max_length=255, null=True, blank=True)
    actor_2 = models.CharField(max_length=255, null=True, blank=True)
    actor_3 = models.CharField(max_length=255, null=True, blank=True)
    actor_4 = models.CharField(max_length=255, null=True, blank=True)
    actor_5 = models.CharField(max_length=255, null=True, blank=True)
    trailer_url = models.URLField(null=True, blank=True)

    class Meta:
        managed = False  # Because we're using an existing table
        db_table = 'movies'