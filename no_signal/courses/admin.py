from django.contrib import admin
from .models import Subject, Course, Module, Lesson


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


class LessonInline(admin.StackedInline):
    model = Lesson


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = (LessonInline,)


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'created')
    list_filter = ('created', 'modified', 'subject')
    search_fields = ('title', 'overview')
    prepopulated_fields = {'slug': ('title',)}
    inlines = (ModuleInline,)
