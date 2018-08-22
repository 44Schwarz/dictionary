from django.shortcuts import render
from .models import Language, Dictionary, Word, Usage


# Create your views here.
def all_dictionaries(request):
    return render(request, 'main/index.html', context={'dictionaries': Dictionary.objects.all()})


def detail(request, dict_id):
    context = {
        'dict': Dictionary.objects.get(pk=dict_id),
        'words': Word.objects.filter(dictionary=dict_id),
    }
    return render(request, 'main/dictionary.html', context=context)
