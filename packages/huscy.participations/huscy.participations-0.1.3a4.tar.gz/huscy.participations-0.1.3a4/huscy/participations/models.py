import enum

from django.db import models
from django.utils.translation import gettext_lazy as _

from huscy.bookings.models import Booking
from huscy.recruitment.models import SubjectGroup


class Participation(models.Model):
    class STATUS(enum.Enum):
        declined = (0, _('Declined'))
        pending = (1, _('Pending'))
        canceled = (2, _('Canceled'))
        finished = (3, _('Finished'))

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    pseudonym = models.CharField(_('Pseudonym'), max_length=64)

    subject_group = models.ForeignKey(SubjectGroup, on_delete=models.PROTECT,
                                      verbose_name=_('Subject group'))

    status = models.IntegerField(_('Status'), choices=[x.value for x in STATUS], default=0)

    class Meta:
        ordering = 'subject_group', 'status'
        verbose_name = _('Participation')
        verbose_name_plural = _('Participations')


class Attendance(models.Model):
    class STATUS(enum.Enum):
        scheduled = (0, _('Scheduled'))
        canceled = (1, _('Canceled'))
        finished = (2, _('Finished'))

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    participation = models.ForeignKey(Participation, on_delete=models.PROTECT,
                                      verbose_name=_('Participation'))
    booking = models.ForeignKey(Booking, on_delete=models.PROTECT, verbose_name=_('Booking'))

    start = models.DateTimeField(_('Start'))
    end = models.DateTimeField(_('End'))

    status = models.IntegerField(_('Status'), choices=[x.value for x in STATUS], default=0)

    class Meta:
        ordering = 'participation', 'status'
        verbose_name = _('Attendance')
        verbose_name_plural = _('Attendances')
