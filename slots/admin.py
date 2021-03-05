from django.contrib import admin
from django.db.models import Count
from django.forms import BaseInlineFormSet
from django.utils.html import format_html

from .models import Reservation, Slot
from .actions import export_as_csv_action, send_email_action

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'slot', 'creation')
    fields = ['first_name', 'last_name', 'email', 'phone', 'slot', 'creation']
    actions = [export_as_csv_action("Exporter en CSV", fields=['id']+fields), send_email_action("Envoyer les emails", template="slots/email2.html")]

    # Display only to super-users
    def has_module_permission(self, request):
        if request.user.is_superuser:  # show for super user anyway
            return True
        else:
            return False

admin.site.register(Reservation, ReservationAdmin)

class ReservationsInline(admin.TabularInline):
    model = Reservation
    readonly_fields = ["creation"]
    extra = 0
    def has_add_permission(self, request, obj=None):
        return obj.free if obj else True

class SlotAdmin(admin.ModelAdmin):

    list_display = ('__str__', 'users', 'url_visio', 'url_presentation_short', 'url_presentation')
    fields = ['description', 'users', 'nb', 'reservation_nb', 'url_visio', 'url_presentation_short', 'url_presentation']
    list_editable = ['users']
    readonly_fields = ["reservation_nb", 'url_visio', 'url_presentation_short', 'url_presentation']
    csv_fields = ['description', 'users', 'nb', 'reservation_nb', 'visio', 'presentation_short', 'presentation']
    actions = [export_as_csv_action("Exporter en CSV", fields=csv_fields)]
    ordering = ('description',)
    inlines = [ReservationsInline]
    save_as = True

    def url_visio(self, obj):
        return format_html('<a href="{0}" target="_blank">{0}</a>', obj.visio)
    url_visio.__name__ = "Lien visio-conférence jitsi"

    def url_presentation(self, obj):
        return format_html('<a href="{0}" target="_blank">{1}</a>', obj.presentation, "Démarrer" if obj.current else "Tester")
    url_presentation.__name__ = "Lancer la présentation"

    def url_presentation_short(self, obj):
        return format_html('<a href="{0}" target="_blank">{0}</a>', obj.presentation_short)
    url_presentation_short.__name__ = "Lien présentation publique"

admin.site.register(Slot, SlotAdmin)
