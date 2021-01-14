from django.urls import path
from . import views

from users import views as user_views

urlpatterns = [
    path('',views.PhotoListView.as_view(),name='index'),
    path('obrazek/<int:pk>/delete/',views.PostDeleteView.as_view(),name='remove'),
    path('user/<str:username>',views.UserPostView.as_view(),name='user-posts'),

    path('add/<str:opcja>', views.add, name='add'),
    path('obrazek/<int:id_obrazka>/',views.detail,name='detail'),
    path('obrazek/<int:id_obrazka>/edit/',views.edit,name='edit'),

]