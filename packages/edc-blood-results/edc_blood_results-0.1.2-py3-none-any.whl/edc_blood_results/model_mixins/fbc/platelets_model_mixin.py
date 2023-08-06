from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO
from edc_reportable import (
    CELLS_PER_MILLIMETER_CUBED,
    CELLS_PER_MILLIMETER_CUBED_DISPLAY,
    TEN_X_9_PER_LITER,
)
from edc_reportable.choices import REPORTABLE


class PlateletsModelMixin(models.Model):
    # platelets
    platelets_value = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9999)],
        null=True,
        blank=True,
    )

    platelets_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=(
            (TEN_X_9_PER_LITER, TEN_X_9_PER_LITER),
            (CELLS_PER_MILLIMETER_CUBED, CELLS_PER_MILLIMETER_CUBED_DISPLAY),
        ),
        null=True,
        blank=True,
    )

    platelets_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    platelets_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
