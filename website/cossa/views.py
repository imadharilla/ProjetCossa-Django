from django.shortcuts import render , redirect
from .models import *
from .forms import * 
from qr_code.qrcode.utils import QRCodeOptions ,ContactDetail



# Create your views here.
from django.http import HttpResponse

def index(request):
    return render(request, 'cossa/index.html')

def reservations(request) :
    if request.user.is_authenticated :
        try :
            reservations_effectues = Reservations.objects.filter(etudiant = request.user.etudiant).order_by('date')
            date_intermediere = reservations_effectues[0].date        
            L = []
            l = []
            l.append(date_intermediere)

            for reservation in reservations_effectues :
                if reservation.date == date_intermediere :
                    print(reservation.repas.nom)
                    l.append(reservation.repas.nom)
                else :
                    L.append(l)
                    date_intermediere = reservation.date
                    l =[]
                    l.append(date_intermediere)
                    l.append(reservation.repas.nom)
            L.append(l)
            date_intermediere = reservation.date
            l =[]
            l.append(date_intermediere)
            l.append(reservation.repas.nom)

                    

            return render(request, 'cossa/reservations.html', { 'reservations' : L , 'pass' :1})
        except :
            return render(request, 'cossa/reservations.html', { 'pass' : 0 })
    else :
        return redirect('/login')


def etudiant_accueil(request):
    Reservations.objects.filter(date__lt=timezone.now()).delete()
    if request.user.is_authenticated :
        try :
            reservations_effectues = Reservations.objects.filter(etudiant = request.user.etudiant).order_by('date')
        except :
            return redirect('/login')
    if request.method == 'POST' and request.user.is_authenticated :
        form = ReForm(request.POST)
        if form.is_valid():
            for repas in form.cleaned_data['repas'] :
                repas = Repas.objects.get(nom= repas)
                current_etudiant = request.user.etudiant
                tomorrow = timezone.now() + timedelta(days=1)
                if form.cleaned_data['date'] < tomorrow.date() :
                    return render(request, 'cossa/accueil_etudiant.html', {'reform' : form , 'reservations' : reservations_effectues, 'erreur':"Vous devez Reserver 24h à l'avance" ,})
                try :
                    
                    Reservations.objects.get(etudiant = current_etudiant, repas = repas, date= form.cleaned_data['date'])
                    
                    return render(request, 'cossa/accueil_etudiant.html', {'reform' : form , 'reservations' : reservations_effectues, 'erreur':"Repas Deja Reservé" ,})
                except :
                    r = Reservations(etudiant = current_etudiant , repas = repas , date= form.cleaned_data['date'])
                    try :
                        current_etudiant.debiter(repas.prix)
                    except :
                        return render(request, 'cossa/accueil_etudiant.html', {'reform' : form , 'reservations' : reservations_effectues, 'erreur':"Solde Insuffisant" ,})

                    r.save()
                    current_etudiant.save()
            return render(request, 'cossa/accueil_etudiant.html', {'reform' : form , 'reservations' : reservations_effectues, 'erreur':"Opération Validée !" ,})
    else :
        form = ReForm(request)

    reform = ReForm(request.POST)

    if request.user.is_authenticated :
        return render(request, 'cossa/accueil_etudiant.html', {'reform' : reform , 'reservations' : reservations_effectues})
   
    else :
        return render(request, 'cossa/accueil_etudiant.html', )



def valider_repas(request) :
    contact_detail = ContactDetail(
        tel= "Matricule : " + str(request.user.etudiant.matricule) + '\n' + "Nom : " + str(request.user.etudiant.nom) ,
    )

    context = dict(
        contact_detail = contact_detail,
        my_options=QRCodeOptions(size='t', border=6, error_correction='L'),
    )
    return render(request, 'cossa/valider_repas.html', context=context)