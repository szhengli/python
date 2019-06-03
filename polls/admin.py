from django.contrib import admin

# Register your models here.

from .models import FrontEnds, Backends
admin.site.register(Backends)
admin.site.register(FrontEnds)


