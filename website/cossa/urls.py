from django.urls import path, include

from . import views
from register import views as register_views
urlpatterns = [
    path('/', views.index, name='index'),
    path('', include("django.contrib.auth.urls")),
    path('/accueil/', views.etudiant_accueil, name='etudiant_accueil'),
    path('/reservations/', views.reservations, name='etudiant_accueil'),
    path('/accueil/valider_repas/', views.valider_repas, name='valider_repas'),
]