from django.db import models
from model_utils.models import TimeStampedModel
# Assuming your curriculum app is in the same project
from django_school_management.curriculum.models import CurriculumLevel, Stream

class AdmissionStudent(TimeStampedModel):
    """
    Model to handle online student admissions linked to the Zambian curriculum.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Curriculum Selection
    target_level = models.ForeignKey(
        CurriculumLevel, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="Grade or Form Applying For"
    )
    
    # Optional stream for Secondary students
    target_stream = models.ForeignKey(
        Stream, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Stream (For Secondary only)"
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    
    remarks = models.TextField(blank=True, help_text="Any additional information from the applicant.")

    class Meta:
        ordering = ['-created']
        verbose_name = 'Student Admission'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.target_level}"

    @property
    def is_secondary(self):
        """Helper to determine if the student is applying for a Secondary level."""
        return self.target_level and self.target_level.stage == 'secondary'
