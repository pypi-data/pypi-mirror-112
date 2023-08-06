from django.db import models
from edc_constants.choices import YES_NO
from edc_reportable import MILLIMOLES_PER_LITER, MILLIMOLES_PER_LITER_DISPLAY
from edc_reportable.choices import REPORTABLE


class UreaModelMixin(models.Model):
    # Serum urea levels
    urea_value = models.DecimalField(
        verbose_name="Urea (BUN)", decimal_places=2, max_digits=6, null=True, blank=True
    )

    urea_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=((MILLIMOLES_PER_LITER, MILLIMOLES_PER_LITER_DISPLAY),),
        null=True,
        blank=True,
    )

    urea_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    urea_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
