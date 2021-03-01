from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid

class Slot(models.Model):

   description = models.CharField("Créneau", max_length=225)
   nb = models.IntegerField("Nombre de créneaux")

   @property
   def reservation_nb(self):
       return self.reservation_set.count()
   reservation_nb.fget.short_description = 'Nombre de créneaux réservés'

   @property
   def free(self):
       return self.reservation_nb < self.nb

   def __str__(self):
       return f"{self.description} ({self.reservation_nb}/{self.nb})"

   class Meta:
       verbose_name = 'Créneau'
       verbose_name_plural = 'Créneaux'

class Reservation(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField("Prénom", max_length=255)
    last_name = models.CharField("Nom", max_length=255)
    email = models.EmailField("Email", unique=True, max_length=255)
    phone_regex = RegexValidator(regex=r'^0\d{9}$', message="Le téléphone doit avoir le format 0123456789")
    phone = models.CharField("Téléphone", validators=[phone_regex], max_length=10, blank=True)
    #def restrict_amount(value):
    #    if Reservation.objects.filter(slot_id=value).count() >= Slot.objects.get(id=value).nb:
    #        raise ValidationError('Créneau plus disponible.')
    slot = models.ForeignKey(Slot, blank=False, verbose_name="Créneau", on_delete=models.CASCADE) #validators=[restrict_amount],
    creation = models.DateTimeField("Date de réservation", default=timezone.now)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    name.fget.short_description = 'Nom'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Réservation'

