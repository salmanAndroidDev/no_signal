from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from courses.views import CourseListView

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('course/', include('courses.urls')),
    path('cms/', include('cms.urls')),
    path('', CourseListView.as_view(), name='course_list'),
    path('students/', include('students.urls')),
    path('api/', include('courses.api.urls', namespace='api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
