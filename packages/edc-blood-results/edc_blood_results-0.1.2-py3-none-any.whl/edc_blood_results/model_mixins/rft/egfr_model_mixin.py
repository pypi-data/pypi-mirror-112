from django.db import models
from edc_constants.choices import YES_NO
from edc_reportable.choices import REPORTABLE


class EgfrModelMixin(models.Model):
    # eGFR
    egfr_value = models.DecimalField(
        verbose_name="eGFR",
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="mL/min/1.73 m2 (system calculated)",
    )

    egfr_units = models.CharField(
        verbose_name="units",
        max_length=15,
        default="mL/min/1.73 m2",
        null=True,
        blank=True,
    )
    egfr_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    egfr_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
