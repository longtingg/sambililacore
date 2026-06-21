from django_countries.fields import CountryField
from model_utils.models import TimeStampedModel
from django_prometheus.models import ExportModelOperationsMixin

from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.urls import reverse

from .utils import model_help_texts

# Localized Zambian Choice Matrixes
PROVINCE_CHOICES = [
    ('central', 'Central Province'),
    ('copperbelt', 'Copperbelt Province'),
    ('eastern', 'Eastern Province'),
    ('luapula', 'Luapula Province'),
    ('lusaka', 'Lusaka Province'),
    ('muchinga', 'Muchinga Province'),
    ('northern', 'Northern Province'),
    ('north_western', 'North-Western Province'),
    ('southern', 'Southern Province'),
    ('western', 'Western Province'),
]

EXAM_BOARD_CHOICES = [
    ('ECZ', 'Examinations Council of Zambia (ECZ)'),
    ('CAMBRIDGE', 'Cambridge Assessment International Education'),
    ('COMBINED', 'Combined ECZ and Cambridge Syllabus'),
]

# Institute Classifications mapping cleanly to Zambian naming structures
INSTITUTE_TYPE_SECONDARY = 'secondary'
INSTITUTE_TYPE_PRIMARY = 'primary'
INSTITUTE_TYPE_COMBINED = 'combined'

INSTITUTE_TYPE_CHOICES = [
    (INSTITUTE_TYPE_SECONDARY, 'Secondary School (Form 1 to 5)'),
    (INSTITUTE_TYPE_PRIMARY, 'Primary School (Grade 1 to 7)'),
    (INSTITUTE_TYPE_COMBINED, 'Combined School (Primary & Secondary Tracks)'),
]

class EducationBoard(ExportModelOperationsMixin('education_board'), models.Model):
    """Education/Examination boards per country for admission forms (e.g., ECZ)."""
    country = CountryField(db_index=True, default='ZM')
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=30, blank=True, help_text='Short code for display (e.g., ECZ)')

    class Meta:
        ordering = ['country', 'name']
        unique_together = [('country', 'name')]

    def __str__(self):
        return f"{self.name} ({self.code})"

    @classmethod
    def get_boards_for_country(cls, country_code):
        """Return boards for a country. For Zambia (ZM), ensures core options exist if empty."""
        if country_code is None:
            return cls.objects.none()
        
        code = getattr(country_code, 'code', country_code) or str(country_code)
        qs = cls.objects.filter(country=code)
        
        # Auto-populate Zambian frameworks if the database table is completely empty
        if code == 'ZM' and not qs.exists():
            zambian_boards = [
                ("Examinations Council of Zambia", "ECZ"),
                ("Cambridge Assessment International Education", "CAMBRIDGE")
            ]
            for name, c in zambian_boards:
                cls.objects.get_or_create(country=code, name=name, defaults={'code': c})
            qs = cls.objects.filter(country=code)
        return qs


class InstituteProfile(ExportModelOperationsMixin('institute_profile'), models.Model):
    name = models.CharField(max_length=255, help_text="Official school name")
    date_of_establishment = models.DateField(blank=True, null=True)
    country = CountryField(default='ZM')
    
    # Regional tracking structures
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES, default='lusaka')
    district = models.CharField(max_length=100, blank=True, help_text="e.g., Lusaka District, Mbala District, Kasama District")
    exam_board = models.CharField(max_length=20, choices=EXAM_BOARD_CHOICES, default='ECZ')
    
    logo = models.ImageField(upload_to='institute/')
    logo_small = models.ImageField(upload_to='institute/', blank=True, null=True)
    site_favicon = models.ImageField(upload_to='institute', blank=True, null=True)
    
    site_header = models.CharField(
        help_text=model_help_texts.INSTITUTE_PROFILE_SITEHEADER,
        max_length=100,
        default=model_help_texts.INSTITUTE_PROFILE_SITEHEADER_DEFAULT
    )
    site_title = models.CharField(
        help_text=model_help_texts.INSTITUTE_PROFILE_SITETITLE,
        max_length=100,
        default=model_help_texts.INSTITUTE_PROFILE_SITETITLE_DEFAULT
    )
    super_admin_index_title = models.CharField(
        help_text=model_help_texts.INSTITUTE_PROFILE_SUPER_ADMIN_INDEX_TITLE,
        max_length=100,
        default=model_help_texts.INSTITUTE_PROFILE_SUPER_ADMIN_INDEX_TITLE_DEFAULT
    )
    
    motto = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=False, unique=True)
    onboarding_completed = models.BooleanField(default=False)
    
    institute_type = models.CharField(
        max_length=20,
        choices=INSTITUTE_TYPE_CHOICES,
        default=INSTITUTE_TYPE_SECONDARY,
        help_text='Determines structural workflow terminology across system templates.',
    )
    
    current_session = models.ForeignKey(
        'academics.AcademicSession',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='institutes_using_as_current',
        help_text='Active operational academic year configuration.',
    )
    curriculum = models.ForeignKey(
        'curriculum.Curriculum',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='institutes',
        help_text='Zambian Ministry CBC Pathway / general framework assignment tracking.',
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.name

    @property
    def onboarding_step(self):
        """Returns the next onboarding configuration module step."""
        if self.onboarding_completed:
            return None
        from django_school_management.academics.models import Department
        if not Department.objects.filter(institute=self).exists():
            return 2
        return 3

    def get_absolute_url(self):
        return reverse('institute:institute_detail', args=[self.pk])

    # Dynamic Terminology Mapping for Zambian School Systems
    @property
    def department_label(self):
        """Translates high-level structural models to match CBC Pathways."""
        return 'CBC Pathway'

    @property
    def department_label_plural(self):
        return 'CBC Pathways'

    @property
    def semester_label(self):
        """Changes terminology from raw semesters to standard Zambian classes (Form/Grade)."""
        if self.institute_type == INSTITUTE_TYPE_SECONDARY:
            return 'Form'
        return 'Grade'

    @property
    def semester_label_plural(self):
        if self.institute_type == INSTITUTE_TYPE_SECONDARY:
            return 'Forms'
        return 'Grades'


class City(ExportModelOperationsMixin('city'), TimeStampedModel):
    """Fallback directory model keeping compatibility with underlying address lookup maps."""
    name = models.CharField(max_length=150)
    country = CountryField(default='ZM')
    code = models.CharField(
        max_length=10,
        help_text='Short provincial or regional system area locator code',
    )

    class Meta:
        verbose_name_plural = 'cities'
        ordering = ['name']
        unique_together = ['country', 'code']

    def __str__(self):
        return self.name
