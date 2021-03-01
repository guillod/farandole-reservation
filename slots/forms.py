from django import forms
from django.core.exceptions import ValidationError

from .models import Reservation, Slot

class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ['first_name', 'last_name', 'email', 'phone', 'slot']
        widgets = {'slot': forms.HiddenInput()}
