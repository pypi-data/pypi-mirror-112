from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO
from edc_reportable import PERCENT
from edc_reportable.choices import REPORTABLE


class HctModelMixin(models.Model):
    # HCT
    hct_value = models.DecimalField(
        validators=[MinValueValidator(1.0), MaxValueValidator(999.0)],
        verbose_name="Hematocrit",
        decimal_places=2,
        max_digits=6,
        null=True,
        blank=True,
    )

    hct_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=((PERCENT, PERCENT),),
        null=True,
        blank=True,
    )

    hct_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    hct_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
