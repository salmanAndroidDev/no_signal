from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from courses.models import Lesson
from core.models import TimeStampedModel
from core.fields import OrderField
from core.constants import GENERIC_RELATED_NAME


class Content(models.Model):
    """Content models that stores different types"""
    lesson = models.ForeignKey(Lesson,
                               related_name=GENERIC_RELATED_NAME,
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'text',
                                         'video',
                                         'image',
                                         'file'
                                     )})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    order = OrderField(blank=True,
                       for_fields='lesson')

    class Meta:
        ordering = ('order',)


class ItemBase(TimeStampedModel):
    """Base abstract mode for content Items"""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=255,
                             blank=True,
                             null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='content/files')


class Image(ItemBase):
    file = models.FileField(upload_to='content/images')


class Video(ItemBase):
    url = models.URLField()
