from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO
from edc_reportable import IU_LITER, IU_LITER_DISPLAY
from edc_reportable.choices import REPORTABLE


class AlpModelMixin(models.Model):
    # ALP
    alp_value = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(999)],
        verbose_name="ALP",
        null=True,
        blank=True,
    )

    alp_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=((IU_LITER, IU_LITER_DISPLAY),),
        null=True,
        blank=True,
    )

    alp_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    alp_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
