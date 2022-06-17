from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Match

admin.site.site_title = _('Ranker Content Management')
admin.site.site_header = _('Ranker Content Management')
admin.site.index_title = _('Content Management')

admin.site.register([Match])
