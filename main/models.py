from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Dictionary(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    language_from = models.ForeignKey(Language, related_name='language_from', on_delete=models.CASCADE)
    language_to = models.ForeignKey(Language, related_name='language_to', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.language_from, self.language_to)

    class Meta:
        verbose_name_plural = 'dictionaries'


class Word(models.Model):
    name = models.CharField(max_length=50)
    definition = models.TextField(blank=True)
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
    translation = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    @property
    def get_usages(self):
        return [obj.text for obj in Usage.objects.filter(word=self)]

    class Meta:
        ordering = ['name']


class Usage(models.Model):
    text = models.TextField()
    word = models.ForeignKey(Word, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.text[:40]) + ' ...' * int(len(self.text) > 40)
