from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', views.PhotoListView.as_view(), name='index'),
    path('user/<str:username>', views.UserPostView.as_view(), name='user-posts'),

    path('obrazek/<int:pk>/', views.ObrazekDetailView.as_view(), name='detail'),

    path('add/<str:opcja>', views.add, name='add'),

    path('obrazek/<int:id_obrazka>/edit/', views.edit, name='edit'),
    path('obrazek/<int:pk>/delete/', views.PostDeleteView.as_view(), name='remove'),

]
