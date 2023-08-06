from django.utils.translation import gettext_lazy as _

from gdaps.api import PluginConfig

from . import __version__


class CorePluginMeta:
    verbose_name = _("MedUX Core")
    author = "Christian González"
    author_email = "christian.gonzalez@nerdocs.at"
    vendor = "nerdocs"
    description = _("Medux Core Plugin")
    category = _("Core")
    visible = True
    version = __version__


class CoreConfig(PluginConfig):
    """MedUX Core Plugin"""

    name = "medux.core"
    PluginMeta = CorePluginMeta

    def ready(self):
        # This function is called after the app and all models are loaded.
        #
        # You can do some initialization here, but beware: it should rather
        # return fast, as it is called at each Django start, even on
        # management commands (makemigrations/migrate etc.).
        #
        # Avoid interacting with the database especially 'save' operations,
        # if you don't *really* have to."""

        try:
            from . import signals
        except ImportError:
            pass
