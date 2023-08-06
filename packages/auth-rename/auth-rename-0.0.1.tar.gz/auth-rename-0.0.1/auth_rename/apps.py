from django.contrib.auth.apps import AuthConfig
from . import __version__ as VERSION

class AuthRenameConfig(AuthConfig):
    verbose_name = "User Management"