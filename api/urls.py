from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ObrazekViewSet,UserProfileViewSet

router = DefaultRouter()
router.register('obrazek', ObrazekViewSet, basename='Obrazek')
router.register('profile',UserProfileViewSet , basename='Obrazek')

urlpatterns = [
    path('', include(router.urls))

]
