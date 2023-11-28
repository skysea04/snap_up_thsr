from basis.db import find_all_models
from django.contrib import admin

# Register your models here.
from . import models as booking_models


class ListAdminMixin:
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(ListAdminMixin, self).__init__(model, admin_site)


for model in find_all_models(booking_models):
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    admin.site.register(model, admin_class)
