from django.contrib import admin
from .models import Gruppo, MembroGruppo, ZoneServizio
from django.db.models import Count  # Importa Count da django.db.models

class MembroGruppoInline(admin.TabularInline):
 
    model = MembroGruppo
    extra = 0

class GruppoInline (admin.TabularInline):
    model = Gruppo
    extra = 0

class ZoneServizioAdmin(admin.ModelAdmin):
    inlines = [GruppoInline]    

class GruppoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cognome', 'numero_telefono','email', 'data_arrivo','indirizzo_soggiorno', 'data_partenza','zona_servizio', 'total_members']
    search_fields = ('nome', 'cognome', 'numero_telefono','indirizzo_soggiorno','zona_servizio')
    list_filter = ('data_arrivo', 'data_partenza','indirizzo_soggiorno','zona_servizio')
    inlines = [MembroGruppoInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(total_members=Count('membrogruppo'))  # Usiamo Count direttamente
        return queryset

    def total_members(self, obj):
        return obj.total_members

    total_members.admin_order_field = 'total_members'
    total_members.short_description = 'Total Members'

class MembroGruppoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cognome', 'gruppo', 'numero_telefono', 'indirizzo_soggiorno', 'data_arrivo', 'data_partenza','zona_servizio')
    search_fields = ('nome', 'cognome', 'numero_telefono','indirizzo_soggiorno')
    list_filter = ('gruppo', 'data_arrivo', 'data_partenza','indirizzo_soggiorno')


class MembroZonaServizio(admin.ModelAdmin):
    list_display = ('nome', 'cognome', 'gruppo', 'numero_telefono', 'indirizzo_soggiorno', 'data_arrivo', 'data_partenza')
    search_fields = ('nome', 'cognome', 'numero_telefono','indirizzo_soggiorno')
    list_filter = ('gruppo', 'data_arrivo', 'data_partenza','indirizzo_soggiorno')

admin.site.register(Gruppo, GruppoAdmin)
 
admin.site.register(MembroGruppo, MembroGruppoAdmin)

admin.site.register(ZoneServizio, ZoneServizioAdmin)