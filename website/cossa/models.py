from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    matricule = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=50)
    prenom =   models.CharField(max_length=50)
    solde = models.FloatField(default=0.0)
    
    def initialiser(self):
        
        self.user = User.objects.csreate_user(username = self.matricule, password = str(self.nom + "@" + self.prenom))
        
    def consulter(self) :
        return self.solde

    def alimenter( self,  valeur ) :
        try:
            valeur is float
        except:
            raise Exception("Ici alimenter, la valeur n'est pas float !")

        self.solde += valeur

    def debiter(self,  valeur):
        try:
            valeur is float
        except:
            raise Exception("Ici debiter, la valeur n'est pas float !")

        
        if self.solde >= valeur :
            self.solde -= valeur
        else:
            raise Exception('solde insuffisant!')
            # missing case !
    
 
    def __str__(self) :
        return self.nom


class Repas(models.Model):
    nom = models.CharField(max_length=15)
    prix = models.FloatField()
    
    def __str__(self): 
        return str(self.nom) +", " + str( self.prix) 


class Reservations(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete = models.CASCADE)
    repas = models.ForeignKey(Repas, on_delete = models.CASCADE)
    date = models.DateField()
    
    def __str__(self):
        return str(self.etudiant) + ", "+ str(self.repas.nom) +", "+ str(self.date)



class Guichetier(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    username = models.CharField(max_length=50, null= False)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)

    def initialiser(self):
        
        self.user = User.objects.csreate_user(username = self.username, password = "zaza2019")
        

    def charger_solde(self, matricule, montant) :
        try :
            a = Etudiant.objects.get(matricule = matricule)
            a.debiter(montant)
        except :
            raise Exception("Etudiant n'existe pas")
        

    def __str__(self) :
        return self.nom

