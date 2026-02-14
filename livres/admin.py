from django.contrib import admin
from .models import Livre, Emprunt

admin.site.register(Livre)
admin.site.register(Emprunt)