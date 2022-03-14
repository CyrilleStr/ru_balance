from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect

from .models import User


class IndexView(generic.TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context


def addUser(request):
    newName = request.POST['name']

    if User.objects.filter(name=newName).exists():
        return render(request, 'main/index.html', {
            'users': User.objects.all(),
            'error_message': "Un utilisateur avec ce nom existe déjà"
        })
    else:
        newUser = User()
        newUser.name = newName
        newUser.save()
        return render(request, 'main/index.html', {
            'users': User.objects.all(),
            'success_message': "Utilisateur bien ajouté"
        })


def addRelation(request):
    return None
