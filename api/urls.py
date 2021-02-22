from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ObrazekViewSet,KometarzeObrazkaViewSet,OcenyObrazkaViewSet,UserProfileViewSet

router = DefaultRouter()
router.register('Obrazek',ObrazekViewSet,basename='obrazek')
router.register('Kometarze_Obrazka',KometarzeObrazkaViewSet,basename='Kometarze_Obrazka')
router.register('Oceny_Obrazka',OcenyObrazkaViewSet,basename='oceny_Obrazka')
router.register('user_profile',UserProfileViewSet,basename='userprofile')

urlpatterns = [
    path('',include(router.urls))

]
