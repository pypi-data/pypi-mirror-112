from django.test.signals import setting_changed
from gdaps.conf import PluginSettings

# This is a default conf file for a GDAPS plugin.
# You can use settings anywhere in your plugin using this syntax:
#
#     from .conf import alerts_settings
#     # or:
#     # from medux.alerts.conf import alerts_settings
#
#     foo = alerts_settings.FOO_SETTING
#
# This way you can use custom (plugin-default) settings, that can be overridden globally if needed.


# required parameter.
NAMESPACE = "ALERTS"

# Optional defaults. Leave empty if not needed.
DEFAULTS = {
    # 'MY_SETTING': 'somevalue',
    # 'FOO_PATH': 'medux.alerts.models.FooModel',
    # 'BAR': [
    #     'baz',
    #     'buh',
    # ],
}

# Optional list of settings keys that are allowed to be in 'string import' notation. Leave empty if not needed.
IMPORT_STRINGS = (
    # 'FOO_PATH',
)

# Optional list of settings that have been removed. Leave empty if not needed.
REMOVED_SETTINGS = ()


alerts_settings = PluginSettings(NAMESPACE, DEFAULTS, IMPORT_STRINGS)


def reload_alerts_settings(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == "ALERTS":
        alerts_settings.reload()


setting_changed.connect(reload_alerts_settings)
