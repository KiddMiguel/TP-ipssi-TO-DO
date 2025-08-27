from django.contrib import admin
from .models import Auteur, Livre

# Register your models here.
class AuteurAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'date_naissance')
    search_fields = ('nom',)

class LivreAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'auteur', 'date_sortie')
    search_fields = ('titre', 'auteur__nom')

admin.site.register(Auteur, AuteurAdmin)
admin.site.register(Livre, LivreAdmin)