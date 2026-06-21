"""
Curriculum library: reusable definitions of curricula, levels, streams, and subjects.
Updated for Zambian Curriculum (Primary Grade 1-6, Secondary Form 1-5).
"""

from model_utils.models import TimeStampedModel
from django_prometheus.models import ExportModelOperationsMixin
from django.db import models

class Curriculum(ExportModelOperationsMixin('curriculum'), TimeStampedModel):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=40, blank=True, help_text='Short code for display.')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveSmallIntegerField(default=0, help_text='Order in lists.')

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name_plural = 'Curricula'

    def __str__(self):
        return self.name

class CurriculumLevel(ExportModelOperationsMixin('curriculum_level'), TimeStampedModel):
    STAGE_CHOICES = [
        ('primary', 'Primary (Grade 1-6)'),
        ('secondary', 'Secondary (Form 1-5)'),
    ]

    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='levels')
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='primary')
    level_number = models.PositiveSmallIntegerField(help_text='Numeric level (1-6 for Primary, 1-5 for Secondary).')
    name = models.CharField(max_length=80, help_text='Display name (e.g. "Grade 1", "Form 1").')
    streams_applicable = models.BooleanField(default=False, help_text='True if subjects defined per stream.')
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['curriculum', 'display_order', 'level_number']
        unique_together = [('curriculum', 'level_number')]

    def __str__(self):
        return f'{self.curriculum}: {self.name}'

class Stream(ExportModelOperationsMixin('stream'), TimeStampedModel):
    name = models.CharField(max_length=60)
    code = models.CharField(max_length=20, unique=True, help_text='e.g. Science, Arts, Commerce.')
    description = models.TextField(blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

class SubjectTemplate(ExportModelOperationsMixin('subject_template'), TimeStampedModel):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=30, unique=True, help_text='Unique code (e.g. MATH, ENG).')
    description = models.TextField(blank=True)
    default_theory_marks = models.PositiveIntegerField(default=100)
    default_practical_marks = models.PositiveIntegerField(default=0)
    is_elective = models.BooleanField(default=False)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return f'{self.name} ({self.code})'

class CurriculumSubject(ExportModelOperationsMixin('curriculum_subject'), TimeStampedModel):
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='curriculum_subjects')
    level = models.ForeignKey(CurriculumLevel, on_delete=models.CASCADE, related_name='subjects')
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, null=True, blank=True, related_name='curriculum_subjects')
    subject_template = models.ForeignKey(SubjectTemplate, on_delete=models.CASCADE, related_name='curriculum_subject_entries')
    is_compulsory = models.BooleanField(default=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['curriculum', 'level', 'stream', 'display_order', 'subject_template']
        constraints = [
            models.UniqueConstraint(
                fields=['curriculum', 'level', 'stream', 'subject_template'], 
                name='unique_curriculum_subject'
            )
        ]
        verbose_name = 'Curriculum subject'
        verbose_name_plural = 'Curriculum subjects'

    def __str__(self):
        stream_part = f' [{self.stream}]' if self.stream else ''
        return f'{self.curriculum} / {self.level}{stream_part}: {self.subject_template}'
