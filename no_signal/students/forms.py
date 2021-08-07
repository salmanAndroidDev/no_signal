from django import forms
from courses.models import Course


class CourseEnrollForm(forms.Form):
    """
        Form to enroll courses
    """
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)
