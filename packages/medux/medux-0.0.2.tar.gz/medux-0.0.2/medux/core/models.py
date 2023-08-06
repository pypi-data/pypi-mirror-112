from django.db import models
from django.contrib.auth.models import AbstractUser

# from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user model for MedUX."""

    class Meta:
        permissions = [("can_login", _("Can login"))]

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
