from django.contrib import admin
from .models import Dictionary, Word, Usage, Language


# Register your models here.
admin.site.register(Dictionary)
admin.site.register(Word)
admin.site.register(Usage)
admin.site.register(Language)
