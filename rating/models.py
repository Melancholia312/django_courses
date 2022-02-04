from django.db import models
from django.conf import settings

from courses.models import Course


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
