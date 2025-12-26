from django.apps import AppConfig


class ExperiencesConfig(AppConfig):
    name = 'experiences'

    def ready(self):
        # =====================================================
        # run create default price types in databse
        # =====================================================
        import experiences.signals
        # =====================================================
