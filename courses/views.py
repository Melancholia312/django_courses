from django import views
from django.db.models import Count, Avg
from .models import Course, Category, UserCourse
from comments.models import Comment
from rating.models import RatingStar, Rating
from django.shortcuts import redirect


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
        categories = self.request.GET.getlist('category')
        if categories:
            queryset = Course.objects.filter(
                category__in=categories
            )
        else:
            queryset = Course.objects.all()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(course=kwargs['object'])
        context['is_student'] = UserCourse.objects.filter(course=kwargs['object'], user=self.request.user).exists()
        context['rating_stars'] = RatingStar.objects.all()
        context['user_rating'] = Rating.objects.filter(course=kwargs['object'], user=self.request.user).first()
        return context


class CourseSignUp(views.View):

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            course = Course.objects.get(id=kwargs['pk'])
            user_course = UserCourse.objects.filter(course=course, user=request.user).exists()
            if not user_course:
                UserCourse.objects.create(course=course, user=request.user)
                return redirect('course_detail', pk=kwargs['pk'])
            else:
                return redirect('course_detail', pk=kwargs['pk'])
        else:
            return redirect('login')

