from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class ZoneServizio(models.Model):
    zona_servizio =models.CharField(max_length=50)

    def __str__(self):
        return self.zona_servizio
   
    class Meta:
        verbose_name = 'Zona Servizio'
        verbose_name_plural = 'Zone Servizio'

class Gruppo(models.Model):
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    numero_telefono = models.CharField(max_length=20)
    indirizzo_soggiorno = models.CharField(max_length=100, blank=True)
    data_arrivo = models.DateField()
    data_partenza = models.DateField()
    zona_servizio = models.ForeignKey(ZoneServizio, on_delete=models.Case, null=True)
    
    def __str__(self):
       return self.nome + ' ' + self.cognome

    class Meta:
        verbose_name = 'Gruppo'
        verbose_name_plural = 'Gruppi'
 

class MembroGruppo(models.Model):
    gruppo = models.ForeignKey(Gruppo, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    numero_telefono = models.CharField(max_length=20)
    indirizzo_soggiorno = models.CharField(max_length=100, blank=True)
    data_arrivo = models.DateField()
    data_partenza = models.DateField()
    zona_servizio = models.ForeignKey(ZoneServizio, on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.zona_servizio:
            self.zona_servizio = self.gruppo.zona_servizio
        super().save(*args, **kwargs)

    
    
    def __str__(self):
        return self.nome + ' ' +self.cognome
    
    class Meta:
        verbose_name = 'Membro'
        verbose_name_plural = 'Membri'

@receiver(post_save, sender=Gruppo)
def update_members_zone(sender, instance, **kwargs):
    # Aggiorna la zona di servizio per tutti i membri del gruppo
    MembroGruppo.objects.filter(gruppo=instance).update(zona_servizio=instance.zona_servizio)