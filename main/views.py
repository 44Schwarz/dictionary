from django.shortcuts import render
from .models import Language, Dictionary, Word, Usage
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
            word = request.POST.get('word')
            if not word:
                return JsonResponse({'done': False})  # return an anchor to indicate that fields are empty

            definition = request.POST.get('definition')
            usage = request.POST.get('usage')
            usgs = usage.split(sep='\n')
            translation = request.POST.get('translation')
            word_id = request.POST.get('word_id')
            w, done = Word.objects.update_or_create(pk=word_id, defaults={'name': word.capitalize(),
                                                                          'translation': translation,
                                                                          'definition': definition})

            if usgs:
                Usage.objects.filter(word=w).delete()
                for us in usgs:
                    if us:
                        Usage.objects.get_or_create(text=us.capitalize(), word=w)

            return JsonResponse({'done': True})

        elif request.method == 'GET':
            context = {
                'dict': Dictionary.objects.get(pk=dict_id),
                'words': Word.objects.filter(dictionary=dict_id),
            }
            return render(request, 'main/dictionary.html', context=context)
    else:
        return HttpResponseForbidden()


@login_required
@require_http_methods(["POST"])
def add_word(request):
    word = request.POST.get('word')
    if not word:
        return JsonResponse({'done': False})  # return an anchor to indicate that fields are empty

    definition = request.POST.get('definition')
    usage = request.POST.get('usage')
    translation = request.POST.get('translation')

    w, done = Word.objects.get_or_create(name=word.capitalize(), dictionary=Dictionary.objects.get(pk=request.POST.get('dict_id')), defaults={'translation': translation, 'definition': definition})
    return JsonResponse({'done': True})


@login_required
@require_http_methods(["POST"])
def delete_word(request):
    try:
        Word.objects.get(pk=request.POST.get('word_id')).delete()
        return JsonResponse({'done': True})
    except:
        return JsonResponse({'done': False})


@login_required
@require_http_methods(["POST"])
def delete_dict(request):
    Dictionary.objects.filter(user=request.user).get(pk=request.POST.get('dict_id')).delete()

    return HttpResponseRedirect(reverse('dictionaries_list'))
