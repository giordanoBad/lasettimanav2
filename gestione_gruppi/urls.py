from django.urls import path
from .views import inserisci_capogruppo, inserisci_membri, home

urlpatterns = [

    path('inserisci_capogruppo/', inserisci_capogruppo, name='inserisci_capogruppo'),
    path('inserisci_membri/', inserisci_membri, name='inserisci_membri'),
    # Altri percorsi URL del tuo progetto...
]
