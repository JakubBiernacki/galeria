from django.apps import AppConfig


class WidokConfig(AppConfig):
    name = 'widok'

    def ready(self):
        import widok.signals
