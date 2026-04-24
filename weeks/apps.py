from django.apps import AppConfig


class WeeksConfig(AppConfig):
    name = 'weeks'

    def ready(self):
        import weeks.signals  # noqa: F401
