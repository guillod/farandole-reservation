import csv
from django.core import mail
from django.http import HttpResponse
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.admin.utils import label_for_field, lookup_field

from .views import textify

from .models import Reservation, Slot

def export_as_csv_action(description="Export selected objects as CSV file", fields=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """

        opts = modeladmin.model._meta

        if fields:
            field_names = fields
        else:
            field_name = [f.name for f in opts.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % str(opts).replace('.', '_')

        writer = csv.writer(response)

        if header:
            writer.writerow([label_for_field(field, modeladmin.model, model_admin=modeladmin) for field in field_names])
        for obj in queryset:
            writer.writerow([lookup_field(field, obj, model_admin=modeladmin)[2] for field in field_names])

        return response

    export_as_csv.short_description = description
    return export_as_csv

def send_email_action(description="Send email", template="slots/email.html"):
    """
    This function send emails to selected persons
    using the default template "slots/email.html"
    """
    def send_email(modeladmin, request, queryset):

        with mail.get_connection() as connection:
            for obj in queryset:
                # email
                html_message =  render_to_string(template, {'form': obj, 'path': request.build_absolute_uri('/')})
                msg = mail.EmailMultiAlternatives(
                   subject = "Portes Ouvertes Crèche Farandole",
                   body =  textify(html_message),
                   from_email = "inscription@crechefarandole.com",
                   to = [obj.email],
                   bcc = ["webmaster@crechefarandole.com"],
                   connection=connection)
                msg.attach_alternative(html_message, "text/html")
                try:
                    msg.send()
                except:
                    messages.error(request, f"Erreur en envoyant à {obj.email}")
        messages.success(request, "Messages envoyés")

    send_email.short_description = description
    return send_email
