# -*- coding: utf-8 -*-

# Django imports
from django.conf import settings
from django.conf.urls import include
from django.urls import path

from tests.config.graphqls.views import CustomGraphQLViewMixin
from tests.config.url_patterns.api import api_urls

# App imports

urlpatterns = [
    path('s/', include([
        path('api/', include(api_urls, namespace='api')),
        path('graphqls/', CustomGraphQLViewMixin.as_view(graphiql=True), name='graphqls'),
    ])),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
