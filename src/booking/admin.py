from django.contrib import admin

from basis.admin import ForeignKeyLinksMixin
from user.admin import UserAdminMixin

# Register your models here.
from .models import HolidayInfo, THSRTicket, BookingRequest


class ListAdminMixin(ForeignKeyLinksMixin):
    def __init__(self, model, admin_site):
        super(ListAdminMixin, self).__init__(model, admin_site)


# for model in find_all_models(booking_models):
#     admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
#     if has_foreign_key_to(model, User):
#         admin_class = type('AdminClass', (ListAdminMixin, UserAdminMixin, admin.ModelAdmin), {})
#     admin.site.register(model, admin_class)

class HolidayInfoAdmin(ListAdminMixin, admin.ModelAdmin):
    list_filter = ('start_reserve_date',)


admin.site.register(HolidayInfo, HolidayInfoAdmin)


class THSRTicketAdmin(ListAdminMixin, UserAdminMixin, admin.ModelAdmin):
    list_filter = ('date', 'created_at')


admin.site.register(THSRTicket, THSRTicketAdmin)


class BookingRequestAdmin(ListAdminMixin, UserAdminMixin, admin.ModelAdmin):
    list_filter = ('status', 'updated_at', 'depart_date')

    class Media:
        js = ('booking/booking_method_toggle.js',)


admin.site.register(BookingRequest, BookingRequestAdmin)
