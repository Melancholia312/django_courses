from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.conf import settings

from courses.models import Course


class Comment(MPTTModel):
    '''Модель отзывов'''

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_comments')
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


class Like(models.Model):
    '''Лайк'''

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'like from {self.user}'