from django.urls import path, include
from rest_framework.routers import DefaultRouter

from inventory import views

router = DefaultRouter()
router.register(r"inventory", views.InventoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
