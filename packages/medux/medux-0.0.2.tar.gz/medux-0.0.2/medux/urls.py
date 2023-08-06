"""medux URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import graphene
import logging
from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers

from gdaps.graphene.schema import GDAPSQuery, GDAPSMutation
from gdaps.pluginmanager import PluginManager
from graphene_django.views import GraphQLView

from medux.core.api import IRestRouter

logger = logging.getLogger(__file__)

# load all schemas from plugins
PluginManager.load_plugin_submodule("schema")

schema = graphene.Schema(query=GDAPSQuery, mutation=GDAPSMutation)

app_name = "medux"

PluginManager.load_plugin_submodule("urls")

# Include Django Rest Framework Routers from plugins
router = routers.DefaultRouter()
for r in IRestRouter:
    router.register(r.url, r.viewset)

urlpatterns = PluginManager.urlpatterns() + [
    path("admin/", admin.site.urls),
    path("graphql/", GraphQLView.as_view(graphiql=settings.DEBUG, schema=schema)),
    path("api/", include(router.urls)),
    path("unicorn/", include("django_unicorn.urls")),
]

if settings.DEBUG:
    try:
        import debug_toolbar

        urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    except ImportError:
        logger.warning(
            "Debug Toolbar not available. Please install it or set DEBUG to False."
        )
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from django.contrib.staticfiles import views
#
# views.serve()
