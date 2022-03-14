from django.urls import path
from django.conf import settings

from . import views

app_name = "main"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("adduser", views.addUser, name="add_user"),
    path("addrelation", views.addRelation, name="add_relation"),
    path("creategenesisblock", views.createGenesisBlockView,
         name="create_genesis_block")
]
