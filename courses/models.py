from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models import Avg


class Category(models.Model):
    '''Модель категории'''

    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)

    def courses_count(self):
        return self.category_courses.count()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Course(models.Model):
    '''Модель курса'''

    name = models.CharField(max_length=150)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_courses')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_courses')
    preview = models.ImageField(upload_to='course/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def reviews_count(self):
        return self.course_comments.count()

    def students_count(self):
        return self.students.count()

    def avg_rating(self):
        return self.ratings.aggregate(Avg('star'))['star__avg']

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'pk': self.id})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class UserCourse(models.Model):
    '''Курс для поступишвего пользоваеля'''

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')
    points = models.IntegerField(default=0)

    def __str__(self):
        return f'course {self.course.name} to {self.user}'

