from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from django_school_management.academics.models import Department, AcademicSession
from django_school_management.institute.forms.institute_profile_form import InstituteProfileCreateForm
from django_school_management.institute.forms.onboarding_forms import (
    OnboardingStep1Form,
    DepartmentFormSet,
    OnboardingAcademicSessionForm,
    LoadSubjectsFromCurriculumForm,
)
from .models import InstituteProfile


def _onboarding_context(current_step):
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
    if hasattr(user, 'institute') and user.institute:
        return user.institute
    active = InstituteProfile.objects.filter(is_active=True).first() or InstituteProfile.objects.filter(active=True).first()
    return active


@login_required
def onboarding_step1(request):
    institute = _resolve_institute(request.user)
    if request.method == 'POST':
        form = OnboardingStep1Form(request.POST, instance=institute)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.active = True
            profile.is_active = True
            if not profile.pk or not profile.created_by_id:
                profile.created_by = request.user
            profile.save()
            return redirect('institute:onboarding_step2')
    else:
        form = OnboardingStep1Form(instance=institute)
    ctx = {'form': form, **_onboarding_context(1)}
    return render(request, 'institute/onboarding/step1.html', ctx)


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
            for dept_form in dept_formset:
                name = dept_form.cleaned_data.get('name', '').strip()
                if name:
                    Department.objects.get_or_create(
                        name=name,
                        institute=institute,
                        defaults={'created_by': request.user}
                    )
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


@login_required
def onboarding_step3(request):
    institute = _resolve_institute(request.user)
    if not institute:
        return redirect('institute:onboarding_step1')
    if request.method == 'POST':
        form = LoadSubjectsFromCurriculumForm(request.POST, institute=institute)
        if form.is_valid():
            return redirect('institute:onboarding_step4')
    else:
        form = LoadSubjectsFromCurriculumForm(institute=institute)
    ctx = {'form': form, **_onboarding_context(3)}
    return render(request, 'institute/onboarding/step3.html', ctx)


@login_required
def onboarding_step4(request):
    institute = _resolve_institute(request.user)
    if not institute:
        return redirect('institute:onboarding_step1')
    if request.method == 'POST':
        if institute:
            institute.onboarding_completed = True
            institute.save()
        return redirect('/')
    ctx = {'institute': institute, **_onboarding_context(4)}
    return render(request, 'institute/onboarding/step4.html', ctx)


class InstituteProfileConfigListView(LoginRequiredMixin, ListView):
    model = InstituteProfile
    template_name = 'institute/dashboard/institute_profile_list.html'
    context_object_name = 'institutes'


class InstituteProfileSetupDashboard(LoginRequiredMixin, View):
    template_name = 'institute/dashboard/setup_school.html'

    def get(self, request):
        form = InstituteProfileCreateForm(request=request)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = InstituteProfileCreateForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            form.save()
            return redirect('institute:institute_profile_list')
        return render(request, self.template_name, {'form': form})


class InstituteProfileConfigDashboard(LoginRequiredMixin, View):
    template_name = 'institute/dashboard/institute_config.html'

    def get(self, request, institute_pk):
        institute = get_object_or_404(InstituteProfile, pk=institute_pk)
        form = InstituteProfileCreateForm(instance=institute, request=request)
        return render(request, self.template_name, {'form': form, 'institute': institute})

    def post(self, request, institute_pk):
        institute = get_object_or_404(InstituteProfile, pk=institute_pk)
        form = InstituteProfileCreateForm(request.POST, request.FILES, instance=institute, request=request)
        if form.is_valid():
            form.save()
            return redirect('institute:institute_config', institute_pk=institute_pk)
        return render(request, self.template_name, {'form': form, 'institute': institute})


class InstituteProfileDetailDashboard(LoginRequiredMixin, DetailView):
    model = InstituteProfile
    template_name = 'institute/dashboard/institute_detail.html'
    context_object_name = 'institute'
    pk_url_kwarg = 'institute_pk'


class SetActiveInstituteProfile(LoginRequiredMixin, View):
    def post(self, request, institute_pk):
        institute = get_object_or_404(InstituteProfile, pk=institute_pk)
        institute.is_active = not institute.is_active
        institute.active = institute.is_active
        institute.save(update_fields=['is_active', 'active'])
        return redirect('institute:institute_profile_list')
