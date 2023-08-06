from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "edc_blood_results_app"
    verbose_name = "Edc Blood Results Sample App"
