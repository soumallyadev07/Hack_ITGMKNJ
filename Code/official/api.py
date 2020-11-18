from .models import Personality
from rest_framework import viewsets, permissions
from .serializers import PersonalitySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

class PersonalityViewSet(generics.ListAPIView):
    queryset = Personality.objects.all()
    filter_backends = [DjangoFilterBackend]
    serializer_class = PersonalitySerializer
    filterset_fields = ['full_name', 'first_name', 'middle_name', 'last_name']

    @classmethod
    def get_extra_actions(cls):
        return []