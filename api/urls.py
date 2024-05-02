from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, HashRequestViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'hashrequests', HashRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
