from django import forms
from django.forms import modelformset_factory
from django_school_management.academics.models import Department, AcademicSession
from django_school_management.curriculum.models import Curriculum
from django_school_management.institute.models import InstituteProfile

DepartmentFormSet = modelformset_factory(
    Department,
    fields=('name', 'short_name', 'code'),
    extra=1
)


class OnboardingStep1Form(forms.ModelForm):
    class Meta:
        model = InstituteProfile
        fields = ['name', 'province', 'district', 'exam_board', 'motto', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False


class OnboardingAcademicSessionForm(forms.ModelForm):
    class Meta:
        model = AcademicSession
        fields = ['year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False


class LoadSubjectsFromCurriculumForm(forms.Form):
    curriculum = forms.ModelChoiceField(
        queryset=Curriculum.objects.all(),
        label="Select Curriculum",
        required=True
    )
    start_class = forms.IntegerField(label="Start Class Number", initial=1)
    end_class = forms.IntegerField(label="End Class Number", initial=12)

    def __init__(self, *args, **kwargs):
        self.institute = kwargs.pop('institute', None)
        super().__init__(*args, **kwargs)

    def get_class_numbers(self):
        start = self.cleaned_data.get('start_class', 1)
        end = self.cleaned_data.get('end_class', 12)
        return range(start, end + 1)
