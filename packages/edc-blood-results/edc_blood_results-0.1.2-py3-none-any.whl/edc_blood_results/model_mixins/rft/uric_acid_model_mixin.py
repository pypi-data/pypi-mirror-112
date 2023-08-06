from django.db import models
from edc_constants.choices import YES_NO
from edc_reportable import (
    MILLIGRAMS_PER_DECILITER,
    MILLIMOLES_PER_LITER,
    MILLIMOLES_PER_LITER_DISPLAY,
)
from edc_reportable.choices import REPORTABLE


class UricModelMixin(models.Model):

    # Serum uric acid levels
    uric_acid_value = models.DecimalField(
        verbose_name="Uric Acid", decimal_places=4, max_digits=10, null=True, blank=True
    )

    uric_acid_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=(
            (MILLIMOLES_PER_LITER, MILLIMOLES_PER_LITER_DISPLAY),
            (MILLIGRAMS_PER_DECILITER, MILLIGRAMS_PER_DECILITER),
        ),
        null=True,
        blank=True,
    )

    uric_acid_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    uric_acid_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
