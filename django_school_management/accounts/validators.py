import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_zambian_nrc(value):
    """Validates Zambian National Registration Card format: NNNNNN/NN/N"""
    if not re.match(r'^\d{6}/\d{2}/\d{1}$', value):
        raise ValidationError(
            _('Enter a valid NRC number in format NNNNNN/NN/N (e.g., 123456/78/9).')
        )


def validate_e164_phone(value):
    """Validates E.164 international phone number format: +[country][number]"""
    if not re.match(r'^\+[1-9]\d{1,14}$', value):
        raise ValidationError(
            _('Enter a phone number in E.164 format (e.g., +260977123456).')
        )
