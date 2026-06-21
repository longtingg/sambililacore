from django import forms
from django.forms import modelformset_factory
from django_school_management.academics.models import Department, AcademicSession, Curriculum
from django_school_management.institute.models import InstituteProfile

# Define the FormSet
DepartmentFormSet = modelformset_factory(
    Department, 
    fields=('name', 'short_name', 'code'), 
    extra=1
)

# ... (Step1 and AcademicSession forms remain the same) ...

class LoadSubjectsFromCurriculumForm(forms.Form):
    # Added common fields for curriculum loading
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
        """Helper to return a range of classes based on inputs."""
        start = self.cleaned_data.get('start_class', 1)
        end = self.cleaned_data.get('end_class', 12)
        return range(start, end + 1)
