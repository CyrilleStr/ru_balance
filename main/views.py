from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.conf import settings

from .models import User, BlockChain, Block

# Rendering IndexView with success/error messages


def renderIndex(request, success_message, error_message):
    if error_message:
        print("error_message"+error_message)
    if success_message:
        print("success_message:"+success_message)
    return render(request, 'main/index.html', {
        'users': User.objects.all().exclude(name="Larchuma"),
        'relations': BlockChain.getAllRelation(),
        'success_message': success_message,
        'error_message': error_message,
    })

# Unique view


class IndexView(generic.TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all().exclude(name="Larchuma")
        context['relations'] = BlockChain.getAllRelation()
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
    creditor = get_object_or_404(User, name=request.POST['borrower'])
    borrower = get_object_or_404(User, name=request.POST['creditor'])
    if creditor == borrower:
        return renderIndex(request, None, "T'as des dettes envers toi-même enculé ?")
    else:
        if not BlockChain.relationExist(creditor, borrower):
            BlockChain.addBlock(Block().createBlock(0, creditor, borrower))
            return renderIndex(request, "Relation bien ajouté ! (le crous en sueur)", None)
        else:
            return renderIndex(request, None, "Ces deux personnes arnaquent déjà le crous !")


def addBlock(request, creditorName, borrowerName, amount):

    try:
        creditor = User.objects.get(name=creditorName)
        borrower = User.objects.get(name=borrowerName)
    except(KeyError, User.DoesNotExist):
        return renderIndex(request, None, "Erreur: rats " + creditorName + " et/ou " + borrowerName + "n'existent pas.")
    if -50 <= int(amount) <= 50:
        BlockChain.addBlock(Block().createBlock(amount, creditor, borrower))
        return renderIndex(request, "Dette bien ajoutée !", None)
    else:
        return renderIndex(request, None, "Montant invalide")

# Create the first block linked to the user "Larchuma"


def createGenesisBlockView(request):
    if Block.objects.all():
        return render(request, 'main/index.html', {
            'users': User.objects.all().exclude(name="Larchuma"),
            'error_message': "Y'a déjà une blockchain"
        })
    else:
        BlockChain.createGenesisBlock()
        return render(request, 'main/index.html', {
            'users': User.objects.all().exclude(name="Larchuma"),
            'success_message': "Blockchain initialisée"
        })
