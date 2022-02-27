from django.db import models
from django.core.validators import FileExtensionValidator
from courses.models import Course


class VideoStep(models.Model):
    '''Шаг курса с видеорядом'''
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='video_steps')
    description = models.TextField(blank=True, null=True)
    file = models.FileField(
        upload_to='video/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    )

    #def get_absolute_url(self):
    #    return reverse('course_detail', kwargs={'pk': self.id})

    def __str__(self):
        return f'video step {self.id} to {self.course}'


class TestStep(models.Model):
    '''Шаг курса с тестом'''
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='test_steps')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'test step {self.id} to {self.course}'

    def questions_count(self):
        return self.questions.count()


class TestQuestion(models.Model):
    '''Вопрос к тесту'''
    test = models.ForeignKey(TestStep, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self):
        return f'question {self.id} to {self.test}'


class QuestionAnswer(models.Model):
    '''Ответ к вопросу'''
    text = models.CharField(max_length=150)
    question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE, related_name='answers')
    is_right = models.BooleanField()

    def __str__(self):
        return f'answer {self.id} to {self.question}'