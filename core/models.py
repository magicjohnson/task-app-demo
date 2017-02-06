from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Task(models.Model):
    OPEN = 'open'
    DONE = 'done'
    STATUS_CHOICES = (
        (OPEN, _('Open')),
        (DONE, _('Done'))
    )
    name = models.CharField(max_length=512, verbose_name=_('Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    status = models.CharField(max_length=64, choices=STATUS_CHOICES, default=OPEN, verbose_name=_('Status'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Created by'), related_name='created_tasks')
    completed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='completed_tasks',
                                     verbose_name=_('Completed by'))

    @property
    def is_done(self):
        return self.status == self.DONE

    def __str__(self):
        return self.name
