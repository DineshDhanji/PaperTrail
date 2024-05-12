from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import Document, Annotaions
from .serializers import AnnotaionsSerializer, DocumentDetailsSerializer


@api_view(["GET"])
def get_annotations(request, doc_id):
    try:
        document = get_object_or_404(Document, pk=doc_id)
    except Http404:
        return Response(
            {"annos": []},
            status=status.HTTP_404_NOT_FOUND,
        )
    serializer = AnnotaionsSerializer(data=document.annotations.all(), many=True)
    serializer.is_valid()  # Ensre data is valid before serialization
    serialized_data = serializer.data  # Access serialized data

    return Response(
        {"annos": serialized_data},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def get_documents(request):
    documents = request.user.docs.all().order_by("-created")
    serializer = DocumentDetailsSerializer(data=documents, many=True)
    serializer.is_valid()  # Ensure data is valid before serialization
    serialized_data = serializer.data  # Access serialized data

    return Response(
        {"docs": serialized_data},
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
                {"message": "Method not allowed", "anno_id": -1},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        try:
            page_number = annotation_data["pageNumber"]
        except:
            page_number = 1

        annotation_instance = Annotaions.objects.create(
            body_value=annotation_data["annotation"]["body"][0]["value"],
            target_selector_value=annotation_data["annotation"]["target"]["selector"][
                "value"
            ],
            doc_id=document,
            annotator=request.user,
            page_number=page_number,
        )
        annotation_instance.save()
        return Response(
            {
                "message": "Annotation created successfully",
                "anno_id": annotation_instance.pk,
            },
            status=status.HTTP_201_CREATED,
        )
    else:
        return Response(
            {"message": "Method not allowed", "anno_id": -1},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


@api_view(["POST"])
def update_annotation(request):
    if request.method == "POST":
        # Assuming you receive annotation data in the request data
        annotation_data = request.data

        document = get_object_or_404(Document, id=annotation_data["doc_id"])
        if not document:
            print("Doc not found")
            return Response(
                {"message": "No such document found.", "anno_id": -1},
                status=status.HTTP_400_BAD_REQUEST,
            )

        annotation_instance = get_object_or_404(
            Annotaions, id=annotation_data["annotation"]["id"]
        )
        if not annotation_instance:
            print("Annotation not found")
            return Response(
                {"message": "No such annotation found.", "anno_id": -1},
                status=status.HTTP_400_BAD_REQUEST,
            )
        annotation_instance.body_value = annotation_data["annotation"]["body"][0][
            "value"
        ]
        annotation_instance.target_selector_value = annotation_data["annotation"][
            "target"
        ]["selector"]["value"]
        annotation_instance.save()
        return Response(
            {
                "message": "Annotation updated successfully",
                "anno_id": annotation_instance.pk,
            },
            status=status.HTTP_202_ACCEPTED,
        )
    else:
        return Response(
            {"message": "Method not allowed", "anno_id": -1},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


@api_view(["POST"])
def delete_annotation(request):
    if request.method == "POST":
        # Assuming you receive annotation data in the request data
        annotation_data = request.data
        document = get_object_or_404(Document, id=annotation_data["doc_id"])
        if not document:
            return Response(
                {"message": "No such document found.", "anno_id": -1},
                status=status.HTTP_400_BAD_REQUEST,
            )

        annotation_instance = get_object_or_404(
            Annotaions, id=annotation_data["annotation"]["id"]
        )
        if not annotation_instance:
            return Response(
                {"message": "No such annotation found.", "anno_id": -1},
                status=status.HTTP_400_BAD_REQUEST,
            )
        annotation_instance.delete()
        return Response(
            {"message": "Annotation deleted successfully"},
            status=status.HTTP_202_ACCEPTED,
        )
    else:
        return Response(
            {"message": "Method not allowed", "anno_id": -1},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


@api_view(["POST"])
def delete_docfile(request):
    if request.method == "POST":

        doc_file_id = request.data["doc_id"]
        document = get_object_or_404(Document, id=doc_file_id)
        if document.owner == request.user:
            document.delete()
            return Response(
                {"message": "Document deleted successfully."},
                status=status.HTTP_202_ACCEPTED,
            )

    return Response(
        {"message": "Method not allowed"},
        status=status.HTTP_405_METHOD_NOT_ALLOWED,
    )
