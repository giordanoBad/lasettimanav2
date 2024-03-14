from django import forms
from .models import Gruppo, MembroGruppo


class GruppoForm(forms.ModelForm):
    numero_membri = forms.IntegerField(label='Numero Membri',help_text="Inserisci il numero di quante persone vuoi aggiungere al tuo gruppo. Se sei solo scrivi 0")
    data_arrivo = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    data_partenza = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    indirizzo_soggiorno = forms.CharField(max_length=100, help_text="Inserisci l'indirizzo di soggiorno del  capogruppo")


    class Meta:
        model = Gruppo
        fields = ['nome', 'cognome', 'numero_telefono', 'email','data_arrivo', 'data_partenza','indirizzo_soggiorno', 'numero_membri']

class MembroGruppoForm(forms.ModelForm):
    data_arrivo = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    data_partenza = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    indirizzo_soggiorno = forms.CharField(max_length=100, help_text="Inserisci l'indirizzo di soggiorno del membro del gruppo")
    class Meta:
        model = MembroGruppo
        fields = ['nome', 'cognome', 'numero_telefono','data_arrivo','data_partenza','indirizzo_soggiorno']
        