from django.urls import path
from . import views

from users import views as user_views

urlpatterns = [
    path('',views.index,name='index'),
    path('add/',views.dodaj,name='dodaj'),
    path('obrazek/<int:id_obrazka>/',views.widok_obrazka,name='widok_obrazka'),
    path('obrazek/<int:id_obrazka>/delete',views.remove,name='remove'),
    path('obrazek/<int:id_obrazka>/edit',views.edit,name='edit'),
]