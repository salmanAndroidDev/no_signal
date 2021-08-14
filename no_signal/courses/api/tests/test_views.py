from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from courses.models import Subject, Course, Module, Lesson
from ..serializers import SubjectSerializer, CourseSerializer, \
    CourseWithContentSerializer
from cms.models import Content, Text

User = get_user_model()


def create_a_dummy_course():
    """Creates a dummy course with content"""
    teacher = User.objects.create_user(email='teacher@gmail.com', password='pass1234')
    subject = Subject.objects.first()
    course_info = {'teacher': teacher, 'subject': subject,
                   'title': 'sample title', 'overview': 'some overview'}
    course = Course.objects.create(**course_info)
    module = Module.objects.create(title='course title', description='course description',
                                   course=course)
    lesson = Lesson.objects.create(title='lesson one', module=module)
    text = Text.objects.create(title='text title', content='actual content', owner=teacher)
    Content.objects.create(item=text, lesson=lesson)
    return course


class APITest(APITestCase):
    """
        Test that API Views works as expected
    """

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(email='user1', password='pass1234')
        self.user2 = User.objects.create_user(email='user2', password='pass1234')

    @classmethod
    def setUpTestData(cls):
        Subject.objects.create(title='title1')
        Subject.objects.create(title='title2')

    def test_subject_list_view(self):
        """
            Test that subject list view works as expected
        """
        URL = reverse('api:subject_list')
        serializer = SubjectSerializer(Subject.objects.all(), many=True)
        response = self.client.get(URL)
        self.assertEqual(response.data, serializer.data)

    def test_subject_detail_view(self):
        """ Test that subject detail view works as expected """
        subject = Subject.objects.first()
        URL = reverse('api:subject_detail', args=[subject.id])
        serializer = SubjectSerializer(subject)

        response = self.client.get(URL)
        self.assertEqual(response.data, serializer.data)

    def test_enroll_course(self):
        """ Test that course enroll view works as expected """
        subject = Subject.objects.first()
        course_info = {'teacher': self.user1, 'subject': subject,
                       'title': 'sample title', 'overview': 'some overview'}
        course = Course.objects.create(**course_info)

        self.client.force_authenticate(self.user2)
        response = self.client.post(f'/api/courses/{course.id}/enroll/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        course.refresh_from_db()
        self.assertIn(self.user2, course.students.all())

    def test_display_courses(self):
        """Test the courses can be displayed successfully"""
        #  Create course #1
        subject = Subject.objects.first()
        course_info = {'teacher': self.user1, 'subject': subject,
                       'title': 'sample title 1', 'overview': 'some overview'}
        Course.objects.create(**course_info)
        #  Create course #2
        course_info = {'teacher': self.user1, 'subject': subject,
                       'title': 'sample title2', 'overview': 'some overview'}
        Course.objects.create(**course_info)
        serializer = CourseSerializer(Course.objects.all(), many=True)

        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_course_content(self):
        """Test that course contents are returned successfully"""
        course = create_a_dummy_course()
        course.students.add(self.user2)
        course.refresh_from_db()
        serializer = CourseWithContentSerializer(course)

        url = f'/api/courses/{course.id}/contents/'
        self.client.force_authenticate(self.user2)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
