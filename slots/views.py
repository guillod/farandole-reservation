from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import re

from .models import Slot, Reservation
from .forms import ReservationForm

def textify(html):
    # Remove html tags and continuous whitespaces
    text_only = re.sub('[ \t]+', ' ', strip_tags(html))
    # Strip single spaces in the beginning of each line
    return text_only.replace('\n ', '\n').strip()

def form_reservation(request, reservation_id=None):

    # get instance on modification
    reservation = get_object_or_404(Reservation, pk=reservation_id) if reservation_id else None

    # on form post
    if request.method == 'POST':
        # instanciate form
        form = ReservationForm(request.POST, request.FILES, instance=reservation)

        if form.is_valid():
            form_instance = form.save(commit=False)
            # slot available
            if form_instance.slot.free:
                # save data
                form_instance.save()
                # email
                html_message =  render_to_string('slots/email.html', {'form': form_instance, 'path': request.build_absolute_uri('/')})
                msg = EmailMultiAlternatives(
                   subject = "Réservation Portes Ouvertes Crèche Farandole",
                   body =  textify(html_message),
                   from_email = "inscription@crechefarandole.com",
                   to = [form_instance.email],
                   bcc = ["webmaster@crechefarandole.com"])
                msg.attach_alternative(html_message, "text/html")
                msg.send()
                #send_mail(subject, message, sender, recipients, html_message=html_message)
                # success
                messages.success(request, f"Réservation effectuée pour {form_instance.slot.description}. Un email de recapitulation vous a été envoyé.")
            else:
                messages.error(request, "Créneau plus disponible. Merci d'en choisir un autre.")
        else:
            messages.error(request, "Erreur en soumettant le formulaire.")
    else:
        form = ReservationForm(instance=reservation)

    slots = Slot.objects.all().order_by('description')
    return render(request, 'slots/form_reservation.html', { 'form': form, 'slots':slots })

def delete_reservation(request, reservation_id):
    # get instance
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    reservation.delete()
    messages.success(request, "Réservation annulée.")
    return redirect("reservation")
