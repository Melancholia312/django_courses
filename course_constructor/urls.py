from django.urls import path
from .views import VideoStepDetailView, StreamingVideo


urlpatterns = [
    path('stream/<int:pk>/', StreamingVideo.as_view(), name='stream'),
    path('video_step/<int:pk>/', VideoStepDetailView.as_view(), name='video'),
]