from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO
from edc_reportable import GRAMS_PER_DECILITER, GRAMS_PER_LITER
from edc_reportable.choices import REPORTABLE


class AlbuminModelMixin(models.Model):  # Serum Albumin
    albumin_value = models.DecimalField(
        decimal_places=1,
        max_digits=6,
        validators=[MinValueValidator(1), MaxValueValidator(999)],
        verbose_name="Serum Albumin",
        null=True,
        blank=True,
    )

    albumin_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=(
            (GRAMS_PER_DECILITER, GRAMS_PER_DECILITER),
            (GRAMS_PER_LITER, GRAMS_PER_LITER),
        ),
        null=True,
        blank=True,
    )

    albumin_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    albumin_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
