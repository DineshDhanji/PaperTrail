from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import Document, ImageAnnotaion
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
    
    return Response( {"annos": serialized_data},
            status=status.HTTP_200_OK,
        )
    
@api_view(["POST"])
def create_annotation(request):
    if request.method == "POST":
        # Assuming you receive annotation data in the request data
        annotation_data = request.data
        document = get_object_or_404(Document, id=annotation_data["doc_id"])
        if not document:
            return Response(
            {"message": "Method not allowed", "anno_id":-1},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
        annotation_instance = ImageAnnotaion.objects.create(
            body_value=annotation_data["annotation"]["body"][0]["value"],
            target_selector_value=annotation_data["annotation"]["target"]["selector"]["value"],
            doc_id = document,
            annotator=request.user,
            )
        annotation_instance.save()
        return Response(
            {"message": "Annotation created successfully", "anno_id": annotation_instance.pk},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {"message": "Method not allowed", "anno_id":-1},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )