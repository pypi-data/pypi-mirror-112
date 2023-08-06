from django import template

register = template.Library()


@register.inclusion_tag("alerts/alert.html")
def toast(title, message, badge=None, icon=None, tag="information", autoclose=False):
    """

    :param context : a dict with the following keys:
        title: the title of the  toast
        message: the message to display
        icon: the icon name to display
        badge: an optional badge
        tag:  one of primary, secondary, light, dark, info, danger, warning, error, critical
        autoclose: if given, the alert will close automatically
    """
    return {
        "title": title,
        "message": message,
        "icon": icon,
        "badge": badge,
        "tag": tag,
        "light_tags": [
            "light",
            "info",
            "warning",
        ],
        "dark_tags": [
            "primary",
            "secondary",
            "danger",
            "dark",
        ],
        "autoclose": bool(autoclose),
    }
