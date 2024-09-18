from django.contrib import admin, messages
from django.db.models import Field, Model
from django.urls import reverse
from django.utils.html import format_html

from .models import ProxyServer, SystemMessage


class ForeignKeyLinksMixin:
    def __init__(self, model: Model, admin_site):
        self.list_display = [
            field.name for field in model._meta.fields
            if not (field.is_relation and field.many_to_one)
        ]
        for field in model._meta.fields:
            field: Field
            if field.is_relation and field.many_to_one:
                self.list_display.insert(model._meta.fields.index(field), 'get_{}'.format(field.name))
                setattr(self, 'get_{}'.format(field.name), self.make_link_func(field))

        super().__init__(model, admin_site)

    def make_link_func(self, field: Field):
        def link_func(obj):
            linked_obj = getattr(obj, field.name)
            linked_obj: Model
            if linked_obj is None:
                return '-'
            url = reverse("admin:{}_{}_change".format(linked_obj._meta.app_label,
                          linked_obj._meta.model_name), args=[linked_obj.pk])
            return format_html('<a href="{}">{}</a>', url, str(linked_obj))

        link_func.short_description = field.verbose_name
        link_func.allow_tags = True
        return link_func


class ListAdminMixin(ForeignKeyLinksMixin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(ListAdminMixin, self).__init__(model, admin_site)


class BaseAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        sys_msg = SystemMessage.get_active()
        if sys_msg:
            messages.add_message(request, sys_msg.level, sys_msg.content)

        return super().changelist_view(request, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        sys_msg = SystemMessage.get_active()
        if sys_msg:
            messages.add_message(request, sys_msg.level, sys_msg.content)

        return super().change_view(request, object_id, form_url, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        sys_msg = SystemMessage.get_active()
        if sys_msg:
            messages.add_message(request, sys_msg.level, sys_msg.content)

        return super().add_view(request, form_url, extra_context)


# register models
class SystemMessageAdmin(ListAdminMixin, BaseAdmin):
    pass


admin.site.register(SystemMessage, SystemMessageAdmin)


class ProxyServerAdmin(ListAdminMixin, BaseAdmin):
    pass


admin.site.register(ProxyServer, ProxyServerAdmin)
