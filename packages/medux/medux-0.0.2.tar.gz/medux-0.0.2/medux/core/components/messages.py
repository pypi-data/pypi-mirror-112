from django.contrib import messages
from django_unicorn.components import UnicornView


class MessagesView(UnicornView):
    def update(self):
        messages.success(self.request, "update called")
