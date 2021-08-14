from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework import status, viewsets
from ..models import Subject, Course
from .serializers import SubjectSerializer, CourseSerializer, \
    CourseWithContentSerializer
from .permissions import IsEnrolled


class SubjectListView(generics.ListAPIView):
    """
        API View to display list of subjects
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    """
        API View to display subject detail
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class CourseEnrollView(APIView):
    """
        API View to enroll courses. only POST method is accepted
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, format=None):
        course = get_object_or_404(Course, id=pk)
        course.students.add(request.user)
        return Response({'enrolled': True}, status=status.HTTP_201_CREATED)


class CourseViewSet(viewsets.ModelViewSet):
    """
        Model ViewSet for to handle course object
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True,
            methods=['post'],
            authentication_classes=[TokenAuthentication],
            permission_classes=[IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
        """enroll action to handle enrolling courses"""
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled': True}, status=status.HTTP_201_CREATED)

    @action(detail=True,
            methods=['get'],
            serializer_class=CourseWithContentSerializer,
            authentication_classes=[TokenAuthentication],
            permission_classes=[IsAuthenticated, IsEnrolled])
    def contents(self, request, *args, **kwargs):
        """Returns course contents"""
        return self.retrieve(request, *args, **kwargs)
