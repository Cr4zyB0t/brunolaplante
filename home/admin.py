from django.contrib import admin

# Register your models here.
from .models import PhotoAccueil, PhotoCategories, PhotoCliches, TypeCategorie, APropos
admin.site.register(PhotoAccueil)
admin.site.register(PhotoCategories)
admin.site.register(PhotoCliches)
admin.site.register(TypeCategorie)
admin.site.register(APropos)