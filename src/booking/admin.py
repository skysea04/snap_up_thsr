from django.contrib import admin

from basis.admin import ForeignKeyLinksMixin
from basis.db import find_all_models, has_foreign_key_to
from user.admin import UserAdminMixin
from user.models import User

# Register your models here.
from . import models as booking_models


class ListAdminMixin(ForeignKeyLinksMixin):
    def __init__(self, model, admin_site):
        super(ListAdminMixin, self).__init__(model, admin_site)


for model in find_all_models(booking_models):
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    if has_foreign_key_to(model, User):
        admin_class = type('AdminClass', (ListAdminMixin, UserAdminMixin, admin.ModelAdmin), {})
    admin.site.register(model, admin_class)
