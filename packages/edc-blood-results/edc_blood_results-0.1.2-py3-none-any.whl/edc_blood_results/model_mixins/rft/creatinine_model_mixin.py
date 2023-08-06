from django.db import models
from edc_constants.choices import YES_NO
from edc_reportable import (
    MICROMOLES_PER_LITER,
    MICROMOLES_PER_LITER_DISPLAY,
    MILLIGRAMS_PER_DECILITER,
)
from edc_reportable.choices import REPORTABLE


class CreatinineModelMixin(models.Model):

    creatinine_value = models.DecimalField(
        decimal_places=2, max_digits=6, null=True, blank=True
    )

    creatinine_units = models.CharField(
        verbose_name="units",
        choices=(
            (MILLIGRAMS_PER_DECILITER, MILLIGRAMS_PER_DECILITER),
            (MICROMOLES_PER_LITER, MICROMOLES_PER_LITER_DISPLAY),
        ),
        max_length=25,
        null=True,
        blank=True,
    )

    creatinine_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    creatinine_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
