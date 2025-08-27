from django.contrib import admin
from .models import Livre, Auteur

# Register your models here.
@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'date_sortie')
    search_fields = ('titre', 'auteur__nom')

@admin.register(Auteur)
class AuteurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_naissance')
    search_fields = ('nom',)
