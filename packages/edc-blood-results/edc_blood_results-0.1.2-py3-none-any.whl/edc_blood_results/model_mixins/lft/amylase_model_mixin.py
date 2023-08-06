from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO
from edc_reportable import IU_LITER, IU_LITER_DISPLAY
from edc_reportable.choices import REPORTABLE


class AmylaseModelMixin(models.Model):
    # Serum Amylase
    amylase_value = models.DecimalField(
        verbose_name="Serum Amylase",
        decimal_places=1,
        max_digits=6,
        validators=[MinValueValidator(0), MaxValueValidator(999)],
        null=True,
        blank=True,
    )

    amylase_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=((IU_LITER, IU_LITER_DISPLAY),),
        null=True,
        blank=True,
    )

    amylase_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    amylase_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
