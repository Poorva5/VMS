from django.apps import AppConfig


class VendorInsightsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vendor_insights"

    def ready(self):
        import vendor_insights.signals