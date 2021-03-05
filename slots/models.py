from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid, hashlib
from django.conf import settings

request = ""

class Slot(models.Model):

    id = models.AutoField(primary_key=True)
    description = models.CharField("Créneau", max_length=225)
    nb = models.IntegerField("Nombre de créneaux")
    users = models.CharField("Familles", blank=True, max_length=225)

    @property
    def reservation_nb(self):
        return self.reservation_set.count()
    reservation_nb.fget.short_description = 'Nombre de créneaux réservés'

    @property
    def free(self):
        return self.reservation_nb < self.nb

    @property
    def date(self):
        return timezone.make_aware(timezone.datetime.strptime(settings.DATE, '%d-%m-%Y'))

    @property
    def start_at(self):
        hours,minutes = self.description.split("h")
        return self.date + timezone.timedelta(hours=int(hours),minutes=int(minutes))

    @property
    def end_at(self):
        return self.start_at + timezone.timedelta(minutes=60)

    @property
    def current(self):
        return self.start_at < timezone.localtime(timezone.now()) < self.end_at

    @property
    def uuid(self):
        namespace = uuid.UUID(settings.UUID)
        return uuid.uuid5(namespace, ""+str(self.id))

    @property
    def short_uuid(self):
        return str(self.uuid).split('-')[0]

    @property
    def visio(self):
        return f"https://meet.jit.si/{self.short_uuid}"

    @property
    def presentation(self):
        relative = reverse("presentation", args=[self.uuid])
        return request.build_absolute_uri(relative)
    presentation.fget.short_description = "Lien présentateur"

    @property
    def presentation_short(self):
        relative = reverse("presentation", args=[self.short_uuid])
        return request.build_absolute_uri(relative)
    presentation_short.fget.short_description = "Lien présentation"

    @property
    def secret(self):
       return str(self.uuid)

    @property
    def socketid(self):
        # SHA256sum of secret
        secret = self.secret.encode()
        return hashlib.sha256(secret).hexdigest()

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
