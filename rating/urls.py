from django.urls import path
from .views import AddRating

urlpatterns = [
    path('course/<int:pk>/add_rating', AddRating.as_view(), name='add_rating'),
]