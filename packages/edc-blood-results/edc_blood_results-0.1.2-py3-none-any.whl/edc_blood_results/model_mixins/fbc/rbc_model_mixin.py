from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO
from edc_reportable import CELLS_PER_MILLIMETER_CUBED, TEN_X_9_PER_LITER
from edc_reportable.choices import REPORTABLE


class RbcModelMixin(models.Model):
    # RBC
    rbc_value = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        validators=[MinValueValidator(1.0), MaxValueValidator(999999.0)],
        verbose_name="Red blood cell count",
        null=True,
        blank=True,
    )

    rbc_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=(
            (TEN_X_9_PER_LITER, TEN_X_9_PER_LITER),
            (CELLS_PER_MILLIMETER_CUBED, CELLS_PER_MILLIMETER_CUBED),
        ),
        null=True,
        blank=True,
    )

    rbc_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    rbc_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
