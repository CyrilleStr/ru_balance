from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.conf import settings

from .models import User, BlockChain, Block

# Unique view


class IndexView(generic.TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all().exclude(name="Larchuma")
        return context

# New user form route


def addUser(request):
    newName = request.POST['name']

    if User.objects.filter(name=newName).exists():
        return render(request, 'main/index.html', {
            'users': User.objects.all().exclude(name="Larchuma"),
            'error_message': "Un rat avec ce blaze existe déjà zebi..."
        })
    else:
        newUser = User()
        newUser.name = newName
        newUser.save()
        return render(request, 'main/index.html', {
            'users': User.objects.all().exclude(name="Larchuma"),
            'success_message': "Rat bien ajouté amdulila !"
        })

# New relation form route
# Adding a new relation <=> creating a 0-amount block with the 2 users


def addRelation(request):
    rat1 = get_object_or_404(User, name=request.POST['borrower'])
    rat2 = get_object_or_404(User, name=request.POST['creditor'])
    if rat1 == rat2:
        return render(request, 'main/index.html', {
            'users': User.objects.all().exclude(name="Larchuma"),
            'error_message': "T'as des dettes envers toi-même enculé ?"
        })
    else:
        bc = BlockChain.objects.all()
        bc[0].addBlock(Block().createBlock(0, rat1, rat2))
        return render(request, 'main/index.html', {
            'users': User.objects.all().exclude(name="Larchuma"),
            'success_message': "Relation bien ajouté ! (le crous en sueur)"
        })

# Create the first block linked to the user "Larchuma"


def createGenesisBlockView(request):
    if BlockChain.objects.all():
        return render(request, 'main/index.html', {
            'users': User.objects.all().exclude(name="Larchuma"),
            'error_message': "Y'a déjà une blockchain"
        })
    else:
        bc = BlockChain()
        bc.createGenesisBlock()
        bc.save()
        return render(request, 'main/index.html', {
            'users': User.objects.all().exclude(name="Larchuma"),
            'success_message': "Blockchain initialisée"
        })
