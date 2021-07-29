from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from ..models import Subject, Course, Module


def create_user(email='sample@email.com', password='pass'):
    """Create a model using email and password"""
    return get_user_model().objects.create_user(
        email=email, password=password)


class TestModels(TestCase):

    def test_subject_generate_slug(self):
        """Test that slug field of Subject gets generated"""
        title = 'auto generate slug filed'
        subject = Subject.objects.create(title=title)
        self.assertEqual(subject.slug, slugify(title))

    def test_subject_add_manually(self):
        """Test that slug field of Subject can be modified manually"""
        title = 'auto generate slug filed'
        different_slug = 'this slug is different'
        subject = Subject.objects.create(title=title, slug=different_slug)
        self.assertEqual(subject.slug, different_slug)

    @classmethod
    def setUpTestData(cls):
        subject = Subject.objects.create(title='title',
                                         slug='title')
        Course.objects.create(teacher=create_user(),
                              subject=subject,
                              title='course',
                              slug='slug')

    def test_module_order_field(self):
        """test that module order works as expected"""
        course = Course.objects.first()
        modules = [Module.objects.create(course=course, title='one'),
                   Module.objects.create(course=course, title='two'),
                   Module.objects.create(course=course, title='three'),
                   Module.objects.create(course=course, title='four'),
                   Module.objects.create(course=course, title='five'),
                   ]

        for index in range(len(modules)):
            self.assertEqual(modules[index].order, index)

        Module.objects.create(course=course, title='ten', order=10)
        Module.objects.create(course=course, title='ten')

        self.assertEqual(Module.objects.last().order, 11)
