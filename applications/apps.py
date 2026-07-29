from django.apps import AppConfig


class ApplicationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications'

    def ready(self):
        # Resource requirements are written against the TOSCA profile, so the
        # columns holding them take their choices from SAT Builder rather than
        # from the database.
        from .field_choices import register
        register()
