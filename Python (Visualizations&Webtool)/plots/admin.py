from django.contrib import admin
from plots.models import Plot, HeatMat
# Register your models here.

admin.site.register([Plot,HeatMat])