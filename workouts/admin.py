from django.contrib import admin
from .models import Training, Exercises, Characteristics

# Register your models here.
admin.site.register(Training)
admin.site.register(Exercises)
admin.site.register(Characteristics)