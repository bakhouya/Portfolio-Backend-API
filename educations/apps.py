from django.apps import AppConfig


class EducationsConfig(AppConfig):
    name = 'educations'

    def ready(self):
        # =====================================================
        # run create default price types in databse
        # =====================================================
        import educations.signals
        # =====================================================
