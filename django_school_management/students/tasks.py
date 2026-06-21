from celery import shared_task
from celery.utils.log import get_logger

from django.core.mail import send_mail
from django.conf import settings

from .models import AdmissionStudent

logger = get_logger(__name__)


@shared_task(name='send_admission_confirmation_email')
def send_admission_confirmation_email(student_id):
    student = AdmissionStudent.objects.get(id=student_id)
    name = student.name
    choosen_dept = student.choosen_department
    send_mail(
        f'Django-School-Management: Admission confirmed for student {name}',
        f'Choosen Dept: {choosen_dept}',
        getattr(settings, 'EMAIL_HOST_USER', 'noreply@example.com'),
        [student.email, ],
        fail_silently=False
    )