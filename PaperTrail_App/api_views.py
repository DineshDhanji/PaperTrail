from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import Document
from .serializers import ImageAnnotaionSerializer

@api_view(["GET"])
def get_annotations(request, doc_id):
    try:
        document = get_object_or_404(Document, pk=doc_id)
    except Http404:
        return Response(
            {"annos": []},
            status=status.HTTP_404_NOT_FOUND,
        )
    serializer = ImageAnnotaionSerializer(data=document.annotations.all(), many=True)
    serializer.is_valid()  # Ensre data is valid before serialization
    serialized_data = serializer.data  # Access serialized data
    
    print(serialized_data)
    return Response( {"annos": serialized_data},
            status=status.HTTP_200_OK,
        )