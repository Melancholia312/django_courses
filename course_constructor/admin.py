from django.contrib import admin
from .models import QuestionAnswer, TestQuestion, TestStep, VideoStep

admin.site.register(QuestionAnswer)
admin.site.register(TestQuestion)
admin.site.register(TestStep)
admin.site.register(VideoStep)