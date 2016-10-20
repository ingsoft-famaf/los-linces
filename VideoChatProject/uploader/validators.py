from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import magic

from . import settings

def validate_file_extension(value):
    metadata = magic.from_buffer(value.file.read(1024)).lower()
    print metadata
    if not any(x in metadata for x in settings.admitted_file_extensions):
        raise ValidationError(_('Invalid file extension'))
