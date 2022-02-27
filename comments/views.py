from .forms import CommentForm
from .models import Comment, Like
from django.shortcuts import redirect
from courses.models import Course
from django import views
from django.views.generic.edit import DeleteView
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from courses.permissions import AuthorPermissionMixin


class AddComment(LoginRequiredMixin, views.View):

    def post(self, request, pk):
        form = CommentForm(request.POST)
        course = Course.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get('parent'))
            form.course = course
            form.user = request.user
            form.save()
        return redirect(course.get_absolute_url())


class CommentDelete(AuthorPermissionMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse_lazy('course_detail', args=[self.object.course_id])


class LikeComment(LoginRequiredMixin, views.View):

    def post(self, request, pk):
        comment = Comment.objects.get(id=pk)
        try:
            Like.objects.get(user=request.user, comment=comment).delete()
        except Like.DoesNotExist:
            Like.objects.create(comment=comment, user=request.user)
        return redirect(comment.course.get_absolute_url())
