from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.form_reservation, name='reservation'),
    path('<uuid:reservation_id>/', views.info_reservation, name='modification'),
    path('<uuid:reservation_id>/change', views.form_reservation, name='modification'),
    path('<uuid:reservation_id>/delete', views.delete_reservation, name='delete'),
    #path('<uuid:reservation_id>/info', views.info_reservation, name='informations'),
    path('<reservation_id>/pres', views.presentation, name='presentation')
]
