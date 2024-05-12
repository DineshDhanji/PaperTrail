from rest_framework import serializers
from .models import User, Annotaions, Document


class AnnotaionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotaions
        fields = "__all__"


class DocumentDetailsSerializer(serializers.ModelSerializer):

    get_doc_link = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ["pk", "doc_name", "created", "owner", "doc_type", "get_doc_link"]

    # Define method to get doc link
    def get_get_doc_link(self, obj):
        return obj.get_doc_link
