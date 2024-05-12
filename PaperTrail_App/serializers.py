from rest_framework import serializers
from .models import User, Annotaions, Document


class AnnotaionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotaions
        fields = "__all__"


class DocumentDetailsSerializer(serializers.ModelSerializer):

    get_doc_link = serializers.SerializerMethodField()
    get_owner_username = serializers.CharField(source="owner.username")

    class Meta:
        model = Document
        fields = [
            "pk",
            "doc_name",
            "created",
            "owner",
            "doc_type",
            "get_doc_link",
            "get_owner_username",
        ]

    # Define method to get doc link
    def get_doc_link(self, obj):
        return obj.get_doc_link


class SharedDocUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "pk",
            "username",
        ]
