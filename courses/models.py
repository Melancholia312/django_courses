from django.db import models
from django.conf import settings
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(models.Model):
    '''Модель категории'''

    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    '''Модель курса'''

    name = models.CharField(max_length=150)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_courses')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_courses')
    preview = models.ImageField(upload_to='course/', blank=True, null=True)
    max_points = models.IntegerField()

    def __str__(self):
        return self.name


class Reviews(MPTTModel):
    '''Модель отзывов'''

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_reviews')
    parent = TreeForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )
    text = models.TextField(max_length=1024)

    def __str__(self):
        return f'review from {self.user} to {self.course.name}'


class RatingStar(models.Model):
    '''Звезда рейтинга'''

    value = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.value}'


class Rating(models.Model):
    '''Рейтинг'''

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_rating_reviews')
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='ratings')

    def __str__(self):
        return f"{self.star} - {self.course}"


class UserCourse(models.Model):
    '''Курс для поступишвего пользоваеля'''

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f'course {self.course.name} to {self.user}'