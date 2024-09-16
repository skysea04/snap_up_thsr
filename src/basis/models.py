from basis.db import BasisModel
from django.contrib.messages.constants import DEFAULT_TAGS
from django.db import models


class SystemMessage(BasisModel):
    content = models.TextField(verbose_name='內容')
    is_active = models.BooleanField(default=True, verbose_name='是否啟用')
    level = models.PositiveSmallIntegerField(choices=DEFAULT_TAGS.items(), verbose_name='等級')

    def __str__(self):
        return self.content

    @classmethod
    def get_active(cls):
        return cls.objects.filter(is_active=True).first()

    class Meta:
        verbose_name = '系統訊息'
        verbose_name_plural = '系統訊息'
