from django.shortcuts import render


# Create your views here.
def all_dictionaries(request):
    return render(request, 'main/index.html')


def detail(request, dict_id):
    return render(request, 'main/dictionary.html')
