from django.urls import resolve
from menu import MenuItem as DjangoMenuItem


class MenuItem(DjangoMenuItem):
    """Custom MenuItem that checks permissions"""

    # def __init__(self, icon="", *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.icon = icon

    def check(self, request):
        """Check permissions based on our view"""
        is_visible = True
        match = resolve(self.url)

        # do something with match, and possibly change is_visible...
        # if self.permission:
        #     self.visible = user.has_perm(self.permission)

        self.visible = is_visible

    def __str__(self):
        return self.title


class MenuSeparator(DjangoMenuItem):
    def __init__(self, *args, **kwargs):
        super().__init__(title="", url="", separator=True, *args, **kwargs)
