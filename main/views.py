from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.conf import settings

from .models import User, Relation

# Rendering IndexView with success/error messages


def renderIndex(request, success_message, error_message):
    if error_message:
        print("error_message"+error_message)
    if success_message:
        print("success_message:"+success_message)
    return render(request, 'main/index.html', {
        'users': User.objects.all().exclude(name="Larchuma"),
        'relations': Relation.objects.all(),
        'success_message': success_message,
        'error_message': error_message,
    })

# Unique view


class IndexView(generic.TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        print(Relation.objects.all())
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all().exclude(name="Larchuma")
        context['relations'] = Relation.objects.all()
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
        if Relation.objects.filter(creditor=creditor, borrower=borrower).exists() or Relation.objects.filter(creditor=borrower, borrower=creditor).exists():
            return renderIndex(request, None, "Ces rats arnquent déjà le crous...")
        else:
            relation = Relation()
            relation.creditor = creditor
            relation.borrower = borrower
            relation.balance = 0
            relation.save()
            return renderIndex(request, "Relation bien ajouté ! (le crous en sueur)", None)


def addBlock(request, creditorName, borrowerName):
    try:
        creditor = User.objects.get(name=creditorName)
        borrower = User.objects.get(name=borrowerName)
        relation = Relation.objects.get(borrower=borrower, creditor=creditor)
    except(KeyError, User.DoesNotExist):
        return renderIndex(request, None, "Erreur: rats " + creditorName + " et/ou " + borrowerName + "n'existent pas ou relation inexistante")
    if request.POST['action'] == "-":
        coeff = -1
    else:
        coeff = 1
    relation.udpateBalance(coeff*float(request.POST['amount']))
    relation.save()
    return renderIndex(request, "Dette bien ajoutée !", None)
