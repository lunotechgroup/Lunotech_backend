from django.contrib import admin
from . import models

admin.site.register(models.Contact)
admin.site.register(models.Project)
admin.site.register(models.Testimonial)
admin.site.register(models.BlogPost)
