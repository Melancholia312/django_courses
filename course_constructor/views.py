from django.shortcuts import render
from django import views
from django.http import StreamingHttpResponse
from .services import open_file
from .models import VideoStep


class VideoStepDetailView(views.generic.DetailView):

    model = VideoStep
    template_name = 'course_consctructor/video_step.html'
    context_object_name = 'video_step'


class StreamingVideo(views.View):

    def get(self, request, *args, **kwargs):

        file, status_code, content_length, content_range = open_file(request, kwargs['pk'])
        response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

        response['Accept-Ranges'] = 'bytes'
        response['Content-Length'] = str(content_length)
        response['Cache-Control'] = 'no-cache'
        response['Content-Range'] = content_range
        return response