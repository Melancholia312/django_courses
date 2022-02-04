from django.shortcuts import render
from django import views
from django.db.models import Q
from django.db.models import Count, Avg
from .models import Course, Category


class Categories:

    def get_categories(self):
        return Category.objects.all()


class Index(views.generic.ListView):

    model = Course
    template_name = 'index.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.annotate(cnt=Count('students'), rate=Avg('ratings')).order_by('-cnt', '-rate')[:3]


class CourseList(Categories, views.generic.ListView):

    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'


class CourseFilter(Categories, views.generic.ListView):

    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        queryset = Course.objects.filter(
            category__in=self.request.GET.getlist('category')
        )
        if self.request.GET.get('order_by') == 'students':
            queryset = queryset.annotate(cnt=Count('students')).order_by('-cnt')
        elif self.request.GET.get('order_by') == 'rating':
            queryset = queryset.annotate(avg=Avg('ratings')).order_by('-avg')
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories_q'] = list(map(int, self.request.GET.getlist('category')))
        context['order_q'] = self.request.GET.get('order_by')
        return context


class CourseSearch(Categories, views.generic.ListView):

    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        queryset = Course.objects.filter(
            name__icontains=self.request.GET.get('q')
        )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search_q'] = self.request.GET.get('q')
        return context


class CourseDetail(views.generic.DetailView):

    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
