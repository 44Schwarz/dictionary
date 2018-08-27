from django.shortcuts import render
from .models import Language, Dictionary, Word, Usage
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse


# Create your views here.
@require_http_methods(["GET", "POST"])
def all_dictionaries(request):
    if request.method == "POST":
        d1 = request.POST.get('language1').capitalize()
        d2 = request.POST.get('language2').capitalize()

        # TODO bug with empty language's names
        if not d1 or not d2:
            return JsonResponse({''})  # return an anchor to indicate that fields are empty

        lang1, _ = Language.objects.get_or_create(name=d1)
        lang2, _ = Language.objects.get_or_create(name=d2)

        dict_new, created = Dictionary.objects.get_or_create(language_from=lang1, language_to=lang2)

        return JsonResponse({'created': created, 'dict_id': dict_new.id, 'dict_name': str(dict_new)})

    return render(request, 'main/index.html', context={'dictionaries': Dictionary.objects.all()})


@require_http_methods(["GET", "POST"])
def detail(request, dict_id):
    if request.method == "POST":
        word = request.POST.get('word').capitalize()
        definition = request.POST.get('definition')
        usage = request.POST.get('usage')
        translation = request.POST.get('translation')
        word_id = request.POST.get('word_id')

        # TODO bug with empty word's names
        if not word:
            return JsonResponse({''})  # return an anchor to indicate that fields are empty

        if word_id:  # edit the existing word
            w = Word.objects.get(id=word_id)
            w.name = word
            w.definition = definition
            w.translation = translation
            w.save()
        else:
            word, created = Word.objects.get_or_create(name=word, dictionary=Dictionary.objects.get(pk=dict_id), defaults={'translation': translation, 'definition': definition})

        # TODO look at update_or_create() method - use it for editing words
        # https://docs.djangoproject.com/en/2.1/ref/models/querysets/#update-or-create

        return JsonResponse({'created': created, 'word': str(word), 'definition': word.definition,
                             'translation': word.translation})

    context = {
        'dict': Dictionary.objects.get(pk=dict_id),
        'words': Word.objects.filter(dictionary=dict_id),
    }
    return render(request, 'main/dictionary.html', context=context)


@require_http_methods(["GET", "POST"])
def detail_word(request, dict_id):
    context = {}
    return render(request, 'main/word.html', context=context)
