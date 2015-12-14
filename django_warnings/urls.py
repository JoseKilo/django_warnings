from django.conf.urls import include, url

from rest_framework import routers

from .views import WarningViewSet


router = routers.SimpleRouter()
router.register(r'warning', WarningViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
