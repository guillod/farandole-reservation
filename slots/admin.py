from django.contrib import admin

from django.contrib import admin
from django.db.models import Count
from django.forms import BaseInlineFormSet

from .models import Reservation, Slot
from .actions import export_as_csv_action

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'slot', 'creation')
    fields = ['first_name', 'last_name', 'email', 'phone', 'slot', 'creation']
    actions = [export_as_csv_action("Exporter en CSV", fields=['id']+fields)]

admin.site.register(Reservation, ReservationAdmin)

class ReservationsInline(admin.TabularInline):
    model = Reservation
    readonly_fields = ["creation"]
    extra = 0
    def has_add_permission(self, request, obj=None):
        return obj.free if obj else True

class SlotAdmin(admin.ModelAdmin):
    list_display = ('description', 'nb', 'reservation_nb')
    fields = ['description', 'nb', 'reservation_nb']
    readonly_fields = ["reservation_nb"]
    actions = [export_as_csv_action("Exporter en CSV", fields=fields)]
    ordering = ('description',)
    inlines = [ReservationsInline]
    save_as = True

admin.site.register(Slot, SlotAdmin)
