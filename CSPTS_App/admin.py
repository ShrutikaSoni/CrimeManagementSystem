from django.contrib import admin
from .models import Fir



@admin.register(Fir)
class FirAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image']