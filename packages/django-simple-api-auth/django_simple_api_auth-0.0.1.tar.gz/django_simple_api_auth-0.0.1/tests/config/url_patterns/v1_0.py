# -*- coding: utf-8 -*-
# Python imports

# Django imports
from django.urls import include, path
# App imports
from rest_framework.routers import DefaultRouter

from django_simple_api_auth.api.rest.v1_0.viewsets import UserApiViewSet

# 3rd Party imports

router = DefaultRouter()

router.register(r'users', UserApiViewSet, 'users')
api_v1_0_urls = (
    [
        path('', include(router.urls)),
    ], 'main_api_v1_0'
)
