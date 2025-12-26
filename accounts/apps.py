from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        # =====================================================
        # run create default price types in databse
        # =====================================================
        import accounts.signals
        # =====================================================
