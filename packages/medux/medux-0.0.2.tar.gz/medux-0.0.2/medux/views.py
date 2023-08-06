# import requests
# from django import http
# from django.conf import settings
# from django.template import engines
from django.views.generic import TemplateView


# def catchall_dev(request, upstream="http://localhost:8080"):
#     upstream_url = upstream + request.path
#     response = requests.get(upstream_url, stream=True)
#     content_type = response.headers.get("Content-Type")
#
#     if content_type == "text/html; charset=UTF-8":
#         return http.HttpResponse(
#             content=engines["django"].from_string(response.text).render(),
#             status=response.status_code,
#             reason=response.reason,
#         )
#
#     else:
#         return http.StreamingHttpResponse(
#             streaming_content=response.iter_content(2 ** 12),
#             content_type=content_type,
#             status=response.status_code,
#             reason=response.reason,
#         )


catchall = TemplateView.as_view(template_name="layouts/base.html")

# catchall = catchall_dev if settings.DEBUG else catchall_prod
