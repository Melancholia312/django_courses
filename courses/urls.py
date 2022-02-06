from django.urls import path
from .views import CourseDetail, CourseList, Index, CourseFilter, CourseSearch, CourseSignUp, UsesCoursesView

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('my_courses/', UsesCoursesView.as_view(), name='user_courses_view'),
    path('courses/', CourseList.as_view(), name='course_list'),
    path('courses/filter/', CourseFilter.as_view(), name='course_filter'),
    path('courses/search/', CourseSearch.as_view(), name='course_search'),
    path('course/<int:pk>/', CourseDetail.as_view(), name='course_detail'),
    path('course/<int:pk>/sign_up/', CourseSignUp.as_view(), name='course_sign_up')
]