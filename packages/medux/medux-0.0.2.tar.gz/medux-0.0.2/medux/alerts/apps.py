import os

# from django.conf import settings
from django.utils.translation import gettext_lazy as _

from gdaps.api import PluginConfig

# from gdaps.frontend.conf import frontend_settings
from . import __version__


class AlertsPluginMeta:
    """This configuration is the introspection data for plugins."""

    # the plugin machine "name" is taken from the AppConfig, so no name here
    verbose_name = _("Alerts")
    author = "Christian González"
    author_email = "christian.gonzalez@nerdocs.at"
    vendor = "Nerdocs"
    description = _("MedUX Alerts plugin")
    category = _("Core")
    visible = True
    version = __version__
    # compatibility = "medux.core>=2.3.0"


class AlertsConfig(PluginConfig):
    """A GDAPS Django app plugin.

    It needs a special parameter named ``PluginMeta``. It is the key for GDAPS
    to recognize this app as a GDAPS plugin.
    ``PluginMeta`` must point to a class that implements certain attributes
    and methods.
    """

    # Dotted Python path to the application, e.g. '/home/christian/Projekte/medux/medux/plugins.fooplugin'
    # It has to start with '/home/christian/Projekte/medux/medux/plugins' to be recognized as plugin.
    name = "medux.alerts"

    # This is the most important attribute of a GDAPS plugin app.
    PluginMeta = AlertsPluginMeta

    def ready(self):
        try:
            from . import signals
        except ImportError:
            pass

        # import implementations of global interfaces
        from . import impl
