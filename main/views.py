from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect

from .models import User


class IndexView(generic.TemplateView):
    template_name = "main/index.html"


def addUser(request):
    newName = request.POST['name']
    if User.ojects.get(name=newName):
        return render(request, 'main/index.html', {
            'error_message': "Un utilisateur avec ce nom existe déjà"
        })
    else:
        newUser = User(name)
        newUser.save()
        return render(request, 'main/index.html', {
            'success_message': "Utilisateur bien ajouté"
        })


def addRelation(request):
    return None
