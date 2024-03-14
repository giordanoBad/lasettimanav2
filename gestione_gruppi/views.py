from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms import inlineformset_factory
from .models import Gruppo, MembroGruppo
from .forms import GruppoForm, MembroGruppoForm
from django.db import transaction


def home(request):
    return render(request, 'gestione_gruppi/inserisci_capogruppo.html')

def inserisci_capogruppo(request):
    if request.method == 'POST':
        gruppo_form = GruppoForm(request.POST)
        if gruppo_form.is_valid():
            capogruppo_data = {
                'nome': gruppo_form.cleaned_data['nome'],
                'cognome': gruppo_form.cleaned_data['cognome'],
                'numero_telefono': gruppo_form.cleaned_data['numero_telefono'],
                'data_arrivo': gruppo_form.cleaned_data['data_arrivo'].strftime('%Y-%m-%d'),
                'data_partenza': gruppo_form.cleaned_data['data_partenza'].strftime('%Y-%m-%d'),
            }
            numero_membri = gruppo_form.cleaned_data['numero_membri']
            # Salviamo temporaneamente i dati del capogruppo e il numero di membri nella sessione
            request.session['capogruppo_data'] = capogruppo_data
            request.session['numero_membri'] = numero_membri
            
            if Gruppo.objects.filter(numero_telefono=gruppo_form.cleaned_data['numero_telefono']).exists() or \
                MembroGruppo.objects.filter(numero_telefono=gruppo_form.cleaned_data['numero_telefono']).exists():
                messages.error(request, 'Il numero di telefono è già associato a un gruppo o a un membro.')
            
            else:

                with transaction.atomic():
                    gruppo_form.save()
                    num_tel = gruppo_form.cleaned_data['numero_telefono']
                    print(num_tel)
                    id_gruppo = Gruppo.objects.get(numero_telefono = num_tel)
                    print(id_gruppo.id)
                    request.session['gruppo_id']=id_gruppo.id 
                    print(request.session['gruppo_id'])
                # Reindirizziamo direttamente alla vista per inserire i membri
                if numero_membri < 1:
                    return render(request, 'gestione_gruppi/conferma_inserimento_membri.html')
                else:
                    return redirect('inserisci_membri')
    else:
        gruppo_form = GruppoForm()
    return render(request, 'gestione_gruppi/inserisci_capogruppo.html', {'gruppo_form': gruppo_form})


def inserisci_membri(request):
    numero_membri = request.session.get('numero_membri', 1)
    gruppo_id = request.session.get('gruppo_id')

    # Recupera il gruppo associato all'ID
    gruppo = Gruppo.objects.get(id=gruppo_id)

    if request.method == 'POST':
        membri_forms = [MembroGruppoForm(request.POST, prefix=f'membro_{i}') for i in range(numero_membri)]
        if all([form.is_valid() for form in membri_forms]):
            #Utilizza una transazione per garantire l'integrità dei dati
            for form in membri_forms:
                    if Gruppo.objects.filter(numero_telefono=form.cleaned_data['numero_telefono']).exists() or \
                        MembroGruppo.objects.filter(numero_telefono=form.cleaned_data['numero_telefono']).exists():
                        messages.error(request, 'Il numero di telefono è già associato a un gruppo o a un membro.')
                    else:
                        
                        with transaction.atomic():
                            for form in membri_forms:
                                form.instance.gruppo = gruppo  # Associa il membro al gruppo corrente
                                form.save()
                        return render(request, 'gestione_gruppi/conferma_inserimento_membri.html')
    else:
        membri_forms = [MembroGruppoForm(prefix=f'membro_{i}') for i in range(numero_membri)]

    return render(request, 'gestione_gruppi/inserisci_membri.html', {'membri_forms': membri_forms})