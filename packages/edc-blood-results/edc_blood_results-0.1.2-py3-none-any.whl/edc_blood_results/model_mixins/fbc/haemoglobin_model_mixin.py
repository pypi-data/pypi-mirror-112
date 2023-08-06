from django.db import models
from edc_constants.choices import YES_NO
from edc_reportable import GRAMS_PER_DECILITER
from edc_reportable.choices import REPORTABLE


class HaemoglobinModelMixin(models.Model):

    # Hb
    haemoglobin_value = models.DecimalField(
        decimal_places=1, max_digits=6, null=True, blank=True
    )

    haemoglobin_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=((GRAMS_PER_DECILITER, GRAMS_PER_DECILITER),),
        null=True,
        blank=True,
    )

    haemoglobin_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    haemoglobin_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
