from django.db import models
from edc_constants.choices import YES_NO
from edc_reportable import GRAMS_PER_DECILITER
from edc_reportable.choices import REPORTABLE


class MchcModelMixin(models.Model):
    # mchc
    mchc_value = models.DecimalField(
        verbose_name="MCHC", decimal_places=2, max_digits=6, null=True, blank=True
    )

    mchc_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=((GRAMS_PER_DECILITER, GRAMS_PER_DECILITER),),
        null=True,
        blank=True,
    )

    mchc_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    mchc_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
