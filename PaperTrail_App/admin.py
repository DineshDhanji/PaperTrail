from django.contrib import admin
from .models import User, Document, ImageAnnotaion

admin.site.register(User)
admin.site.register(Document)
admin.site.register(ImageAnnotaion)
