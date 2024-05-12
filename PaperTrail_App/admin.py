from django.contrib import admin
from .models import User, Document, Annotaions

class AnnotaionsAdminPanel(admin.ModelAdmin):
    list_display = [
        "pk",
        "annotator",
        "get_doc_pk",
        "get_doc_name",
        "get_doc_type",
    ]

    def get_doc_pk(self, obj):
        return obj.doc_id.pk

    def get_doc_type(self, obj):
        return obj.doc_id.doc_type

    def get_doc_name(self, obj):
        return obj.doc_id.doc_name

    # Renameing of fields
    get_doc_pk.short_description = "Doc ID"
    get_doc_type.short_description = "Doc Type"
    get_doc_name.short_description = "Doc Name"


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
admin.site.register(Annotaions, AnnotaionsAdminPanel)
