from django.contrib import admin
from .models import Category, Course, UserCourse, Rating, RatingStar, Reviews


admin.site.register(RatingStar)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(UserCourse)
admin.site.register(Rating)
admin.site.register(Reviews)

