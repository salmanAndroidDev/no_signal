from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from .models import Course, Module, Subject
from .forms import ModuleFormSet, LessonFormSet
from students.forms import CourseEnrollForm


class OwnerMixin(object):
    """
        Mixin to get the queryset created by current user
    """

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(teacher=self.request.user)


class OwnerEdiMixin(object):
    """
        Mixin to set owner to the current when form validation was successful
    """

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin,
                       LoginRequiredMixin,
                       PermissionRequiredMixin):
    """
        Base Mixin for all Course views
    """
    model = Course
    fields = ('subject', 'title', 'overview', 'image')
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEdiMixin):
    """
        Mixin that renders the form to create and edit Course
    """
    template_name = 'manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, generic.ListView):
    """
        ListView that renders current user courses
    """
    template_name = 'manage/course/list.html'
    permission_required = 'courses.view_course'


class CourseCreateView(OwnerCourseEditMixin, generic.CreateView):
    """
        CreateView to create new courses
    """
    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin, generic.UpdateView):
    """
        UpdateView to update existing courses
    """
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, generic.DeleteView):
    """
        DeleteView to delete courses
    """
    template_name = 'manage/course/delete.html'
    permission_required = 'courses.delete_course'


class BaseCourseMixin(object):
    """
        Mixin to initialize course object before calling get or post
    """
    course = None

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course,
                                        id=pk,
                                        teacher=request.user)
        return super().dispatch(request, pk)


class CourseModuleUpdateView(BaseCourseMixin, TemplateResponseMixin, View):
    """
        View to update course modules
    """
    template_name = 'manage/module/formset.html'

    def get_formset(self, data=None):
        """Initialize the form with the current course"""
        return ModuleFormSet(instance=self.course,
                             data=data)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('course_module_list', self.course.id)
        return self.render_to_response({'course': self.course,
                                        'formset': formset})


class CourseManageModules(BaseCourseMixin, OwnerMixin, generic.DetailView):
    """
        View to manage modules
    """
    template_name = 'manage/module/list.html'
    model = Course


class CourseLessonUpdateView(TemplateResponseMixin, View):
    """
        View to update course lessons
    """
    template_name = 'manage/lesson/formset.html'
    module = None

    def dispatch(self, request, pk):
        """Initialize module before calling get & post"""
        self.module = get_object_or_404(Module,
                                        id=pk)
        return super().dispatch(request, pk)

    def get_formset(self, data=None):
        """Initialize the form with the current course"""
        return LessonFormSet(instance=self.module,
                             data=data)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'module': self.module,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('course_module_list', self.module.course.id)
        return self.render_to_response({'module': self.module,
                                        'formset': formset})


class CourseListView(TemplateResponseMixin, View):
    """
        View to show list of available courses
    """
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        subjects = Subject.objects.annotate(
            total_courses=Count('courses'))
        courses = Course.objects.annotate(
            total_modules=Count('modules'))

        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response({'subjects': subjects,
                                        'subject': subject,
                                        'courses': courses})


class CourseDetailView(generic.DetailView):
    """
        View to display Course details
    """
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(
            initial={'course': self.object})
        return context
