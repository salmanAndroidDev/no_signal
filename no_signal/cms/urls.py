from django.urls import path
from . import views

urlpatterns = [
    path('lesson/<int:lesson_id>/content/<model_name>/create/',
         views.ContentCreateUpdateView.as_view(),
         name='lesson_content_create'),

    path('lesson/<int:lesson_id>/content/<model_name>/create/<id>/',
         views.ContentCreateUpdateView.as_view(),
         name='lesson_content_update'),

    path('content/<int:id>/delete/',
         views.ContentDeleteView.as_view(),
         name='lesson_content_delete'),

    path('lesson/<int:lesson_id>/',
         views.LessonContentListView.as_view(),
         name='lesson_content_list')
]
