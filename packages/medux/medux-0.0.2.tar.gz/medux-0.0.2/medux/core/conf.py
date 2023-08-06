from django.test.signals import setting_changed
from gdaps.conf import PluginSettings

NAMESPACE = "CORE"

DEFAULTS = {}
IMPORT_STRINGS = ()
REMOVED_SETTINGS = ()

core_settings = PluginSettings(NAMESPACE, DEFAULTS, IMPORT_STRINGS)


def reload_core_settings(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == "CORE":
        core_settings.reload()


setting_changed.connect(reload_core_settings)
