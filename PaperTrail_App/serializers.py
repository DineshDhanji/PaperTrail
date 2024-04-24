from rest_framework import serializers 
from .models import User,  ImageAnnotaion

class ImageAnnotaion(serializers.ModelSerializer):
    class Meta:
        model = ImageAnnotaion
        fields = "__all__"