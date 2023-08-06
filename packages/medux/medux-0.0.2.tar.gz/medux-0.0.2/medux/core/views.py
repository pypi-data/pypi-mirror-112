# from django.contrib.auth import get_user_model
# User = get_user_model()
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from medux.core.api import IViewMode, IGlobalJavascript


class MeduxBaseMixin(PermissionRequiredMixin):
    """Mixin for all views that MedUX uses.

    Inherit from this view if you want to create a new page etc. in MedUX.
    You have to specify the `permission_required`attribute, since all MedUX views
    need to have a permission for seeing it.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "viewmodes": iter(IViewMode),
                "global_javascripts": iter(IGlobalJavascript),
            }
        )
        return context


class HomeView(MeduxBaseMixin, TemplateView):
    template_name = "home.html"
    # FIXME find a correct permission for home, and use MeduxBaseMixin
    permission_required = ()
    extra_context = {
        "viewmodes": iter(IViewMode),
    }
