from django.forms.models import modelform_factory
from django.apps import apps
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View
from courses.models import Lesson
from .models import Content


class ContentCreateUpdateView(TemplateResponseMixin, View):
    """
        Manage creating generic contents
    """
    lesson = None
    model = None
    obj = None
    template_name = 'manage/lesson/form.html'

    def get_model(self, model_name):
        """Find current model"""
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model('cms', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        """Get a generic form"""
        Form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'created',
                                                 'modified'])
        return Form(*args, **kwargs)

    def dispatch(self, request, lesson_id, model_name, id=None):
        self.lesson = get_object_or_404(Lesson,
                                        id=lesson_id,
                                        module__course__teacher=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)

        return super().dispatch(request, lesson_id, model_name, id)

    def get(self, request, lesson_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

    def post(self, request, lesson_id, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                Content.objects.create(lesson=self.lesson,
                                       item=obj)
            return redirect('lesson_content_list', self.lesson.id)
        return self.render_to_response({'form': form,
                                        'object': form})


class ContentDeleteView(View):
    """
        View to delete content
    """

    def post(self, request, id):
        content = get_object_or_404(Content,
                                    id=id,
                                    lesson__module__course__teacher=request.user)
        lesson = content.lesson
        content.item.delete()
        content.delete()
        return redirect('lesson_content_list', lesson.id)


class LessonContentListView(TemplateResponseMixin, View):
    """
        View to manage content
    """
    template_name = 'manage/lesson/content_list.html'

    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lesson,
                                   id=lesson_id,
                                   module__course__teacher=request.user)
        return self.render_to_response({'lesson': lesson})
