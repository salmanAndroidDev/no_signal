from django.db import models
from django.conf import settings
from django.utils.text import slugify
from core.models import TimeStampedModel
from core.constants import GENERIC_RELATED_NAME
from core.fields import OrderField


class AutoSaveMixin(object):
    """
        Model mixin to auto save slug field from title
    """

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(AutoSaveMixin, self).save(*args, **kwargs)


class Subject(AutoSaveMixin, models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,
                            unique=True,
                            blank=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Course(AutoSaveMixin, TimeStampedModel):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='courses_created',
                                on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name=GENERIC_RELATED_NAME,
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,
                            unique=True,
                            blank=True)
    overview = models.TextField()
    image = models.FileField(upload_to='courses/%Y/%m/%d/',
                             blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name=GENERIC_RELATED_NAME,
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    order = OrderField(blank=True,
                       for_fields='course')

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return f'{self.order}. {self.title}'


class Lesson(models.Model):
    module = models.ForeignKey(Module,
                               related_name=GENERIC_RELATED_NAME,
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    order = OrderField(blank=True,
                       for_fields='module')

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return f'{self.title}. {self.title}'
