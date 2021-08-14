from rest_framework import serializers
from ..models import Subject, Course, Module, Lesson
from cms.serializers import ContentSerializer


class SubjectSerializer(serializers.ModelSerializer):
    """
        Subject Model serializer
    """

    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']


class LessonSerializer(serializers.ModelSerializer):
    """
        Lesson Model serializer
    """

    class Meta:
        model = Lesson
        fields = ('order', 'title')


class ModuleSerializer(serializers.ModelSerializer):
    """
        Module Model serializer
    """
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ('order', 'title', 'description', 'lessons')


class CourseSerializer(serializers.ModelSerializer):
    """
        Course Model serializer
    """
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview',
                  'created', 'teacher', 'modules']


class LessonWithContentSerializer(serializers.ModelSerializer):
    """
        Lesson serializer that returns contents
    """
    contents = ContentSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ['order', 'title', 'contents']


class ModuleWithContentSerializer(serializers.ModelSerializer):
    """
        Module serializer that returns contents
    """
    lessons = LessonWithContentSerializer(many=True)

    class Meta:
        model = Module
        fields = ['order', 'title', 'description', 'lessons']


class CourseWithContentSerializer(serializers.ModelSerializer):
    """
        Course serializer that returns contetns
    """
    modules = ModuleWithContentSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview',
                  'created', 'teacher', 'modules']
