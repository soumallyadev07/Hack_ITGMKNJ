from rest_framework import routers
from .api import PersonalityViewSet
from django.urls import path
from .views import csv_to_dbsql

router = routers.DefaultRouter()
router.register('api/personalities', PersonalityViewSet)

urlpatterns = [
    path('api/personalities', PersonalityViewSet.as_view(), name='personalities'),
    path('db/personalities/', csv_to_dbsql, name='csv_to_db'),
]