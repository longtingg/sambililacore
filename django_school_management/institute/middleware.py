import re
from django_school_management.institute.models import InstituteProfile

_SLUG_PREFIX_RE = re.compile(r'^/s/([^/]+)(?:/|$)')


class AttachInstituteDataMiddleware:
    """
    Per-request middleware that attaches the resolved InstituteProfile to the
    template context as ``request_institute``.

    Resolution order:
    1. Authenticated user's ``User.institute`` FK (school-scoped context)
    2. URL slug prefix  /s/<slug>/  (direct school URL routing)
    3. First ``is_active=True`` institute (multi-tenant fallback)
    4. Legacy fallback: first ``active=True`` institute
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_template_response(self, request, response):
        try:
            institute = self._resolve(request)
            if response.context_data is not None:
                response.context_data['request_institute'] = institute
        except Exception:
            pass
        return response

    def _resolve(self, request):
        if request.user.is_authenticated:
            inst = getattr(request.user, 'institute', None)
            if inst:
                return inst

        m = _SLUG_PREFIX_RE.match(request.path)
        if m:
            try:
                return InstituteProfile.objects.get(slug=m.group(1))
            except InstituteProfile.DoesNotExist:
                pass

        inst = InstituteProfile.objects.filter(is_active=True).first()
        if inst:
            return inst

        return InstituteProfile.objects.filter(active=True).first()
