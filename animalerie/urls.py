from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_accueil, name="accueil"),
    path("animal/<str:pk>/", views.animal_detail, name="animal_detail"),
    path("equipement/<str:pk>/", views.equipment_detail, name="equipment_detail"),
    path("animal/<str:pk>/?<str:message>", views.animal_detail, name="animal_detail_mes"),
]
