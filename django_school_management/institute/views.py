from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django_school_management.academics.models import Department, AcademicSession
from django_school_management.institute.forms.institute_profile_form import InstituteProfileCreateForm
from django_school_management.institute.forms.onboarding_forms import (
    OnboardingStep1Form,
    DepartmentFormSet, 
    OnboardingAcademicSessionForm,
    LoadSubjectsFromCurriculumForm,
)
from .models import InstituteProfile

# ──────────────────────────────────────────────
# Helper Functions (Required by your views)
# ──────────────────────────────────────────────

def _onboarding_context(current_step):
    """Generates the progress bar steps for the onboarding wizard."""
    steps = [
        {'number': 1, 'title': 'Institute Profile'},
        {'number': 2, 'title': 'Academics'},
        {'number': 3, 'title': 'Load Subjects'},
        {'number': 4, 'title': 'Review'},
    ]
    step_data = []
    for s in steps:
        step_data.append({
            **s,
            'status': 'completed' if s['number'] < current_step
            else 'active' if s['number'] == current_step
            else 'upcoming',
        })
    return {'onboarding_steps': step_data, 'current_step': current_step}

def _resolve_institute(user):
    """Find the active institute associated with the user."""
    # Check if user has an attached institute
    if hasattr(user, 'institute') and user.institute:
        return user.institute
    
    # Fallback to the active profile in the system
    active = InstituteProfile.objects.filter(active=True).first()
    return active

# ──────────────────────────────────────────────
# Step 2 View
# ──────────────────────────────────────────────

@login_required
def onboarding_step2(request):
    institute = _resolve_institute(request.user)
    if not institute:
        return redirect('institute:onboarding_step1')

    existing_departments = Department.objects.filter(institute=institute)
    existing_session = AcademicSession.objects.order_by('-year').first()

    if request.method == 'POST':
        dept_formset = DepartmentFormSet(request.POST, prefix='departments')
        session_form = OnboardingAcademicSessionForm(request.POST, instance=existing_session)
        
        if dept_formset.is_valid() and session_form.is_valid():
            # Save Departments
            for dept_form in dept_formset:
                name = dept_form.cleaned_data.get('name', '').strip()
                if name:
                    Department.objects.get_or_create(
                        name=name, 
                        institute=institute, 
                        defaults={'created_by': request.user}
                    )
            # Save Session
            session = session_form.save(commit=False)
            session.created_by = request.user
            session.save()
            return redirect('institute:onboarding_step3')
    else:
        dept_formset = DepartmentFormSet(prefix='departments')
        session_form = OnboardingAcademicSessionForm(instance=existing_session)

    ctx = {
        'dept_formset': dept_formset,
        'session_form': session_form,
        'existing_departments': existing_departments,
        **_onboarding_context(2),
    }
    return render(request, 'institute/onboarding/step2.html', ctx)
