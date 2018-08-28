from django.shortcuts import render
from .models import Language, Dictionary, Word
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.http.response import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin


# Create your views here.
@login_required
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

        dict_new, created = Dictionary.objects.get_or_create(language_from=lang1, language_to=lang2, user=request.user)

        return JsonResponse({'created': created, 'dict_id': dict_new.id, 'dict_name': str(dict_new)})

    return render(request, 'main/index.html', context={'dictionaries': Dictionary.objects.filter(user=request.user)})


@login_required
# @user_passes_test(dict_owner_check)
@require_http_methods(["GET", "POST"])
def detail(request, dict_id):
    if request.user == Dictionary.objects.get(pk=dict_id).user:
        if request.method == 'POST':
            if request.POST.get('add') == 'true':
                word = request.POST.get('word')
                if not word:
                    return JsonResponse({'done': False})  # return an anchor to indicate that fields are empty

                definition = request.POST.get('definition')
                usage = request.POST.get('usage')
                translation = request.POST.get('translation')
                w, done = Word.objects.get_or_create(name=word.capitalize(),
                                                     dictionary=Dictionary.objects.get(pk=dict_id),
                                                     defaults={'translation': translation, 'definition': definition})

            word_id = request.POST.get('word_id')

            # TODO bug with empty word's names

            if word_id:  # edit or delete the existing word
                w = Word.objects.get(id=word_id)
                if request.POST.get('delete'):  # delete
                    w.delete()
                    done = True
                else:  # edit
                    word = request.POST.get('word')
                    if not word:
                        return JsonResponse({'done': False})  # return an anchor to indicate that fields are empty

                    definition = request.POST.get('definition')
                    usage = request.POST.get('usage')
                    translation = request.POST.get('translation')

                    w.name = word.capitalize()
                    w.definition = definition
                    w.translation = translation
                    w.save()
                    done = True
            else:  # add a new word (or update existing but via form for adding a new one)
                w, done = Word.objects.get_or_create(name=word.capitalize(), dictionary=Dictionary.objects.get(pk=dict_id), defaults={'translation': translation, 'definition': definition})

            # TODO look at update_or_create() method - use it for editing words
            # https://docs.djangoproject.com/en/2.1/ref/models/querysets/#update-or-create

            return JsonResponse({'done': done, 'word': str(w), 'definition': word.definition,
                                 'translation': word.translation})

        elif request.method == 'GET':
            context = {
                'dict': Dictionary.objects.get(pk=dict_id),
                'words': Word.objects.filter(dictionary=dict_id),
            }
            return render(request, 'main/dictionary.html', context=context)
    else:
        return HttpResponseForbidden()


@login_required
@require_http_methods(["GET", "POST"])
def add_word(request):
    # TODO dict_id
    word = request.POST.get('word')
    if not word:
        return JsonResponse({'done': False})  # return an anchor to indicate that fields are empty

    definition = request.POST.get('definition')
    usage = request.POST.get('usage')
    translation = request.POST.get('translation')

    w, done = Word.objects.get_or_create(name=word.capitalize(), dictionary=Dictionary.objects.get(pk=dict_id),
                                         defaults={'translation': translation, 'definition': definition})
    return JsonResponse({})


@login_required
@require_http_methods(["POST"])
def delete_dict(request):
    Dictionary.objects.filter(user=request.user).get(pk=request.POST.get('dict_id')).delete()

    return HttpResponseRedirect(reverse('dictionaries_list'))
