from django import forms
from .models import * 
from bootstrap_datepicker_plus import DatePickerInput


class DateInput(forms.DateInput):
    input_type = 'date'

class ReForm(forms.Form) :
    date = forms.DateField(widget=DateInput)
    mini_tuple = ()
    pere_tuple = ()
    for repas in Repas.objects.all() :
        mini_tuple = repas.nom , repas.nom
        pere_tuple = pere_tuple + (mini_tuple,)

    
    repas = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices= pere_tuple ,
    )


    class Meta:
        model = Reservations
        fields = ['date', 'repas']
