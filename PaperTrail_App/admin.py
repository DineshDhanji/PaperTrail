from django.contrib import admin
from .models import User, Document, ImageAnnotaion


class DocumentAdminPanel(admin.ModelAdmin):
    list_display = [
        "doc_name",
        "doc_type",
        "get_owner_username",
        "pk",
    ]

    def get_owner_username(self, obj):
        return obj.owner.username

    # Renameing of fields
    get_owner_username.short_description = "Owner"


# Register your models here.
admin.site.register(User)
admin.site.register(Document, DocumentAdminPanel)
admin.site.register(ImageAnnotaion)
