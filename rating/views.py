from .models import Rating, RatingStar
from courses.models import Course
from django import views
from django.shortcuts import redirect


class AddRating(views.View):

    def post(self, request, pk):
        star = RatingStar.objects.get(value=request.POST.get('rating'))
        course = Course.objects.get(id=pk)
        if star:
            Rating.objects.update_or_create(course=course, user=request.user, defaults={'star': star})
        return redirect(course.get_absolute_url())