from rest_framework import viewsets, permissions
from .models import Auteur, Livre
from .serializers import AuteurSerializer, LivreSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class AuteurViewSet(viewsets.ModelViewSet):
    queryset = Auteur.objects.all()
    serializer_class = AuteurSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Action personnalisée: /auteurs/<id>/titres/
    @action(detail=True, methods=['get'])
    def titres(self, request, pk=None):
        auteur = self.get_object()
        titres = list(auteur.livres.values_list('titre', flat=True))
        return Response({'titres': titres})

    def get_queryset(self):
        qs = Auteur.objects.all()
        year = self.request.query_params.get('year', None)
        if year and year.isdigit():
            qs = qs.filter(date_naissance__year__gt=int(year))
        return qs

class LivreViewSet(viewsets.ModelViewSet):
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
