from django.db import models
from edc_constants.choices import YES_NO
from edc_reportable.choices import REPORTABLE
from edc_reportable.units import PICOGRAMS_PER_CELL


class MchModelMixin(models.Model):
    # mch
    mch_value = models.DecimalField(
        verbose_name="MCH", decimal_places=2, max_digits=6, null=True, blank=True
    )

    mch_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=((PICOGRAMS_PER_CELL, PICOGRAMS_PER_CELL),),
        null=True,
        blank=True,
    )

    mch_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    mch_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
