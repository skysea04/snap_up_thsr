import inspect
from typing import List

from django.db import models


def find_all_models(module) -> List[models.Model]:
    str_module_members = dir(module)
    model_lst = []
    for str_member in str_module_members:
        member = getattr(module, str_member)
        if not inspect.isclass(member) or not issubclass(member, models.Model):
            continue
        if member._meta.abstract:
            continue
        if member.__module__ != module.__name__:  # Skip imported models
            continue

        model_lst.append(member)

    return model_lst


def has_foreign_key_to(model: models.Model, to_model: models.Model):
    for field in model._meta.get_fields():
        if field.get_internal_type() == 'ForeignKey' and field.related_model == to_model:
            return True
    return False


class BasisModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
