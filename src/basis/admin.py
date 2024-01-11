from django.db.models import Field, Model
from django.urls import reverse
from django.utils.html import format_html


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
