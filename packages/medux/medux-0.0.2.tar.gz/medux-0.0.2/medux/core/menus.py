from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from menu import Menu

from medux.core.api import IViewMode
from medux.core.api.menus import MenuItem, MenuSeparator

__all__ = ["menu_patient", "menu_extras__settings", "menu_notifications"]


class SearchViewMode(IViewMode):
    title = _("Search")
    url = "/search"
    icon = "bi-search"
    weight = 20


# Patient menu
_menu_patient__new = MenuItem(
    title=_("New"),
    url=reverse("home"),
    weight=0,
    icon="bi-person-circle",
)
menu_patient = MenuItem(
    title=_("Patient"),
    url=reverse("home"),
    weight=0,
    children=[
        _menu_patient__new,
        MenuSeparator(),
    ],
)
Menu.add_item("main_menu", menu_patient)

# Extras
menu_extras__settings = MenuItem(
    _("Settings"),
    reverse("home"),
    slug="settings",
    weight=10,
    icon="bi-gear",
    icon_only=True,
)
menu_extras = MenuItem(
    _("Extras"), url=reverse("home"), weight=30, children=[menu_extras__settings]
)
Menu.add_item("main_menu", menu_extras)


# top right menu
menu_notifications = MenuItem(
    _("Notifications"),
    url=reverse("home"),
    weight=20,
    icon="bi-bell",
    icon_only=True,
    badge=True,  # FIXME: this shouldn't be hardcoded here
)
Menu.add_item(
    "top_navbar",
    menu_notifications,
)


Menu.add_item(
    "top_navbar",
    MenuItem(
        title=lambda request: request.user,
        url=reverse("home"),
        slug="myaccount",
        weight=99,
        icon="bi-user",
        children=[
            MenuItem("Edit Profile", url=reverse("home"), icon="bi-user"),
            MenuItem(
                title="Admin",
                url=reverse("admin:index"),
                # check=lambda request: request.user.is_superuser,
            ),
            MenuSeparator(),
            MenuItem(
                title=_("Logout"),
                url=reverse("logout"),
                icon="bi-box-arrow-right",
            ),
        ],
    ),
)
