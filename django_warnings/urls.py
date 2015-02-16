from django.conf.urls import patterns, include, url

from rest_framework import routers

from .views import WarningViewSet


router = routers.SimpleRouter()
router.register(r'warning', WarningViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
)
