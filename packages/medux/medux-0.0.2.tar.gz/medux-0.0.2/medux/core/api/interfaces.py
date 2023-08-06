from gdaps.api import Interface


@Interface
class IViewMode:
    """Interface for MedUX ViewModes.

    A ViewMode provides data and methods for displaying an icon for the
    main viewing modes of MedUX.
    """

    __service__ = True

    #: The title which is displayed when hovering over the icon.
    title = ""

    #: the URL that should be called. Can be a Dajngo reverse() URL.
    url = ""

    #: the icon as text, using Bootstrap Icons
    icon = "bi-file-earmark"

    #: icon_type determines where the icon is fetched from:
    #: bi (Bootstrap icon) or png, then it is loaded from static files
    icon_type = "bi"  # png

    #: the weight of the icon in the list. The higher the weight, the "deeper" the icon.
    weight = 0


@Interface
class IGlobalJavascript:
    """Interface for adding Js file to a global scope.

    The given file will be loaded in the global context and is then available to
    all other plugins too, in every loaded page.
    Be aware just to add Js code that is small and fast, to not blow up the application
    as whole.

    You have to specify the (relative to static dir) file path of the Js script in the
    `file` attribute.
    """

    __service__ = True

    #: The (relative to static dir) file path of the Js script
    file: str = ""


@Interface
class IRestRouter:
    """Interface for collecting Django Rest Framework routers under one global URL.

    Just provide an URL and the viewset, and MedUX registers this router into the
    DefaultRouter.
    """

    url = ""
    viewset = None
